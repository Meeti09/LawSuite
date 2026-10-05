from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..ai.intake import run_intake
from ..rag.retriever import retrieve, grounded_answer
from .. import schemas

router = APIRouter(prefix="/api/legal-help", tags=["legal-help"])


@router.post("/chat")
def chat(body: schemas.ChatIn, db: Session = Depends(get_db)):
    history = [{"role": "user", "content": body.message}]
    if body.matter_id:
        msgs = db.query(models.MatterMessage).filter_by(matter_id=body.matter_id).order_by(models.MatterMessage.created_at).all()
        history = [{"role": m.role, "content": m.content} for m in msgs] + history
    result = run_intake(history, body.language or "en")
    # RAG grounding
    sources = db.query(models.LegalSource).filter_by(status="ACTIVE").all()
    docs = retrieve(body.message, sources)
    rag = grounded_answer(body.message, docs)
    return {"ok": True, "data": {**result, "grounding": rag}}


@router.post("/intake")
def intake(body: schemas.ChatIn, db: Session = Depends(get_db)):
    return chat(body, db)
