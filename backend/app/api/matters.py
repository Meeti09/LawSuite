from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets
from ..database import get_db
from .. import models, auth

router = APIRouter(prefix="/api/matters", tags=["matters"])


@router.post("")
def create_matter(payload: dict, db: Session = Depends(get_db)):
    m = models.LegalMatter(title=payload.get("title", "New matter")[:300], category=payload.get("category"),
                           language=payload.get("language", "en"), state=payload.get("state"),
                           status="Understanding", summary=payload.get("summary", {}),
                           handoff_token=secrets.token_hex(16))
    db.add(m); db.commit(); db.refresh(m)
    return {"ok": True, "data": {"id": m.id, "status": m.status, "handoff_token": m.handoff_token}}


@router.get("")
def list_matters(db: Session = Depends(get_db)):
    rows = db.query(models.LegalMatter).order_by(models.LegalMatter.created_at.desc()).limit(50).all()
    return {"ok": True, "data": [{"id": m.id, "title": m.title, "category": m.category, "status": m.status, "created_at": str(m.created_at)} for m in rows]}


@router.get("/handoff/{token}")
def by_handoff(token: str, db: Session = Depends(get_db)):
    m = db.query(models.LegalMatter).filter_by(handoff_token=token).first()
    if not m: raise HTTPException(404, "Invalid handoff token")
    return {"ok": True, "data": {"id": m.id, "title": m.title, "category": m.category, "summary": m.summary}}
