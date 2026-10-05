from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import secrets
from ..database import get_db
from .. import models, schemas, auth
from ..whatsapp.provider import get_whatsapp, GREETINGS, next_state, STATES
from ..ai.intake import run_intake
from ..config import settings, WHATSAPP_DEEP_LINK

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


@router.get("/info")
def info():
    url = settings.WHATSAPP_BUSINESS_URL or WHATSAPP_DEEP_LINK
    return {"ok": True, "data": {"number": settings.WHATSAPP_NUMBER, "url": url, "provider": settings.WHATSAPP_PROVIDER}}


@router.post("/simulate")
def simulate(payload: dict, db: Session = Depends(get_db)):
    """Mock WhatsApp conversation: drives the real state machine without Meta API."""
    phone = payload.get("phone", "919000000000")
    text = (payload.get("message") or "").strip()
    lang = payload.get("language", "en")
    if not text:
        return {"ok": True, "data": {"reply": "Please type a message to continue.", "state": "START"}}
    conv = db.query(models.WhatsAppConversation).filter_by(phone=phone).order_by(models.WhatsAppConversation.created_at.desc()).first()
    is_new = not conv or conv.status == "RESOLVED"
    if is_new:
        conv = models.WhatsAppConversation(phone=phone, language=lang, state="START", status="AI_HANDLING",
                                            handoff_token=secrets.token_hex(12))
        db.add(conv); db.flush()
    db.add(models.WhatsAppMessage(conversation_id=conv.id, direction="IN", body=text))
    facts = dict(conv.facts or {})
    turns = list(facts.get("turns", [])) + [text]
    facts["turns"] = turns
    conv.facts = facts
    trivial = text.lower().strip(" !.,") in ("hi", "hello", "hey", "yo", "hii", "start", "namaste", "namaskar", "sat sri akal")
    greet = GREETINGS.get(conv.language or lang, GREETINGS["en"])
    if is_new and trivial:
        reply = greet
        conv.state = "LANGUAGE_SELECTION"
    else:
        history = [{"role": "user", "content": t} for t in turns[-5:]]
        res = run_intake(history, conv.language or lang)
        conv.category = res["brief"]["category"]
        base = conv.state if conv.state in STATES else "START"
        conv.state = next_state(base if not is_new else "LANGUAGE_SELECTION")
        reply = res["reply"]
        if is_new:
            reply = greet + "\n\n" + reply
        if conv.state in ("LAWYER_OPTION", "COMPLETED"):
            reply += f"\n\nContinue on web with this token: /legal-help?handoff={conv.handoff_token}"
            if "lawyer" in text.lower():
                conv.status = "LAWYER_REQUESTED"
    db.add(models.WhatsAppMessage(conversation_id=conv.id, direction="OUT", body=reply))
    db.commit()
    get_whatsapp().send_message(phone, reply)
    return {"ok": True, "data": {"reply": reply, "state": conv.state, "category": conv.category or "", "handoff_token": conv.handoff_token, "conversation_id": conv.id}}


@router.api_route("/webhook", methods=["GET", "POST"])
def webhook(request: Request, db: Session = Depends(get_db)):
    """Meta Cloud API compatible verify + receive stub."""
    return {"ok": True, "data": {"status": "webhook active (mock). Configure WHATSAPP_PROVIDER=cloud + tokens for production."}}
