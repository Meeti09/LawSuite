from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..services.documents import render, TEMPLATES, DISCLAIMER

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("/types")
def types():
    return {"ok": True, "data": [{"key": k, **v} for k, v in TEMPLATES.items()]}


@router.post("/generate")
def generate(body: schemas.DocGenIn, db: Session = Depends(get_db)):
    if body.doc_type not in TEMPLATES:
        raise HTTPException(400, "Unknown document type")
    content = render(body.doc_type, body.fields)
    d = models.GeneratedDocument(user_id=None, matter_id=body.matter_id, doc_type=body.doc_type,
                                 title=TEMPLATES[body.doc_type]["title"], content=content)
    db.add(d); db.commit(); db.refresh(d)
    return {"ok": True, "data": {"id": d.id, "title": d.title, "content": content, "disclaimer": DISCLAIMER}}
