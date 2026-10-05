from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/admin", tags=["admin"])
Admin = auth.require_roles("ADMIN")


@router.get("/overview")
def overview(db: Session = Depends(get_db), _=Depends(Admin)):
    return {"ok": True, "data": {
        "total_users": db.query(models.User).count(),
        "lawyers": db.query(models.Lawyer).count(),
        "verified_lawyers": db.query(models.Lawyer).filter_by(verification_status="VERIFIED").count(),
        "pending_verifications": db.query(models.Lawyer).filter_by(verification_status="PENDING").count(),
        "consultations": db.query(models.LawyerRequest).count(),
        "matters": db.query(models.LegalMatter).count(),
        "documents": db.query(models.GeneratedDocument).count(),
        "whatsapp_conversations": db.query(models.WhatsAppConversation).count(),
        "note": "Seeded/demo data is labelled in seed script."}}


@router.get("/lawyers")
def pending(db: Session = Depends(get_db), _=Depends(Admin)):
    rows = db.query(models.Lawyer).order_by(models.Lawyer.created_at.desc()).all()
    return {"ok": True, "data": [{"id": l.id, "full_name": l.full_name, "enrollment_number": l.enrollment_number,
        "city": l.city, "state": l.state, "status": l.verification_status, "created_at": str(l.created_at)} for l in rows]}


@router.patch("/lawyers/{lid}/verify")
def verify(lid: str, body: schemas.VerifyIn, db: Session = Depends(get_db), admin=Depends(Admin)):
    l = db.query(models.Lawyer).filter_by(id=lid).first()
    if not l: raise HTTPException(404, "Not found")
    mapping = {"APPROVE": "VERIFIED", "REJECT": "REJECTED", "MORE_INFO": "PENDING", "SUSPEND": "SUSPENDED"}
    l.verification_status = mapping.get(body.action, "PENDING")
    l.verification_notes = body.notes
    auth.audit(db, admin.id, "ADMIN", body.action, "lawyer", lid, body.notes)
    db.commit()
    return {"ok": True, "data": {"id": l.id, "status": l.verification_status}}


@router.get("/whatsapp")
def wa_list(db: Session = Depends(get_db), _=Depends(Admin)):
    rows = db.query(models.WhatsAppConversation).order_by(models.WhatsAppConversation.created_at.desc()).limit(50).all()
    return {"ok": True, "data": [{"id": c.id, "phone_masked": (c.phone[:4] + "****" + c.phone[-2:]), "language": c.language,
        "category": c.category, "state": c.state, "status": c.status, "created_at": str(c.created_at)} for c in rows]}


@router.get("/audit")
def audit_list(db: Session = Depends(get_db), _=Depends(Admin)):
    rows = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(100).all()
    return {"ok": True, "data": [{"action": a.action, "entity": a.entity, "entity_id": a.entity_id, "detail": a.detail, "created_at": str(a.created_at)} for a in rows]}
