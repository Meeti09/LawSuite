from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..rag.retriever import retrieve, grounded_answer

router = APIRouter(prefix="/api/legal-research", tags=["research"])


@router.post("/search")
def search(body: schemas.ResearchIn, db: Session = Depends(get_db)):
    sources = db.query(models.LegalSource).filter_by(status="ACTIVE").all()
    docs = retrieve(body.query, sources, {"act": body.act or "", "category": body.category or "", "year": body.year or ""})
    r = grounded_answer(body.query, docs)
    return {"ok": True, "data": r}


@router.get("/sources")
def sources(db: Session = Depends(get_db)):
    rows = db.query(models.LegalSource).filter_by(status="ACTIVE").limit(50).all()
    return {"ok": True, "data": [{"id": s.id, "title": s.title, "act": s.act, "section": s.section, "category": s.category, "source_url": s.source_url, "simple_explanation": s.simple_explanation} for s in rows]}
