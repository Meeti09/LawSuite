from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/lawyers", tags=["lawyers"])

def slugify(name, enroll):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{s}-{enroll.lower().replace('/','-')}"


@router.get("")
def list_lawyers(practice_area: str = "", city: str = "", state: str = "", language: str = "", min_exp: int = 0, db: Session = Depends(get_db)):
    q = db.query(models.Lawyer).filter_by(verification_status="VERIFIED")
    if city: q = q.filter(models.Lawyer.city.ilike(f"%{city}%"))
    if state: q = q.filter(models.Lawyer.state.ilike(f"%{state}%"))
    if min_exp: q = q.filter(models.Lawyer.experience_years >= min_exp)
    rows = q.all()
    out = []
    for l in rows:
        pas = [r.practice_area for r in db.query(models.LawyerPracticeArea).filter_by(lawyer_id=l.id).all()]
        langs = [r.language for r in db.query(models.LawyerLanguage).filter_by(lawyer_id=l.id).all()]
        if practice_area and practice_area not in pas: continue
        if language and language not in langs: continue
        out.append({"id": l.id, "slug": l.slug, "full_name": l.full_name, "photo_url": l.photo_url,
                    "city": l.city, "state": l.state, "experience_years": l.experience_years,
                    "practice_areas": pas, "languages": langs, "bio": (l.bio or "")[:220],
                    "availability": l.availability, "verified": True, "rating": l.rating})
    return {"ok": True, "data": out}


@router.get("/{slug}")
def detail(slug: str, db: Session = Depends(get_db)):
    l = db.query(models.Lawyer).filter_by(slug=slug).first()
    if not l or l.verification_status != "VERIFIED":
        raise HTTPException(404, "Lawyer not found")
    pas = [r.practice_area for r in db.query(models.LawyerPracticeArea).filter_by(lawyer_id=l.id).all()]
    langs = [r.language for r in db.query(models.LawyerLanguage).filter_by(lawyer_id=l.id).all()]
    return {"ok": True, "data": {"id": l.id, "slug": l.slug, "full_name": l.full_name, "email": l.email,
        "city": l.city, "state": l.state, "experience_years": l.experience_years, "firm": l.firm,
        "bio": l.bio, "courts": l.courts, "availability": l.availability, "practice_areas": pas,
        "languages": langs, "verified": True, "trust": ["Enrollment verified", "Identity verified", "Profile reviewed"]}}


@router.post("/register")
def register(body: schemas.LawyerRegisterIn, db: Session = Depends(get_db)):
    slug = slugify(body.full_name, body.enrollment_number)
    if db.query(models.Lawyer).filter_by(slug=slug).first():
        raise HTTPException(400, "Already registered with this enrollment")
    l = models.Lawyer(slug=slug, full_name=body.full_name, email=body.email, phone=body.phone,
                      city=body.city, state=body.state, enrollment_number=body.enrollment_number,
                      experience_years=body.experience_years, firm=body.firm, bio=body.bio,
                      courts=body.courts, availability=body.availability or "Available",
                      verification_status="PENDING")
    db.add(l); db.flush()
    for pa in body.practice_areas: db.add(models.LawyerPracticeArea(lawyer_id=l.id, practice_area=pa))
    for lg in body.languages: db.add(models.LawyerLanguage(lawyer_id=l.id, language=lg))
    for d in body.documents: db.add(models.LawyerVerification(lawyer_id=l.id, document_type=d.get("type", "certificate"), document_url=d.get("url", "")))
    db.commit()
    return {"ok": True, "data": {"id": l.id, "slug": l.slug, "status": "PENDING", "message": "Your profile is under review."}}


@router.post("/request")
def request_consult(body: schemas.LawyerRequestIn, db: Session = Depends(get_db)):
    l = db.query(models.Lawyer).filter_by(id=body.lawyer_id).first()
    if not l: raise HTTPException(404, "Lawyer not found")
    r = models.LawyerRequest(lawyer_id=l.id, matter_id=body.matter_id, issue_summary=body.issue_summary, status="PENDING")
    db.add(r); db.commit(); db.refresh(r)
    return {"ok": True, "data": {"id": r.id, "status": r.status, "message": "Consultation requested. Payment integration ready (not charged in demo)."}}
