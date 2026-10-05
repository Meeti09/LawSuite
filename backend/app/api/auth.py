from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(body: schemas.RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=body.email.lower()).first():
        raise HTTPException(400, "Email already registered")
    role = body.role if body.role in ("USER", "LAWYER") else "USER"
    u = models.User(name=body.name, email=body.email.lower(), phone=body.phone,
                    password_hash=auth.hash_password(body.password), role=role)
    db.add(u); db.commit(); db.refresh(u)
    return {"ok": True, "data": {"token": auth.make_token(u), "role": u.role, "name": u.name, "id": u.id}}


@router.post("/login")
def login(body: schemas.LoginIn, db: Session = Depends(get_db)):
    u = db.query(models.User).filter_by(email=body.email.lower()).first()
    if not u or not auth.verify_password(body.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"ok": True, "data": {"token": auth.make_token(u), "role": u.role, "name": u.name, "id": u.id}}


@router.post("/admin-login")
def admin_login(body: schemas.LoginIn, db: Session = Depends(get_db)):
    u = db.query(models.User).filter_by(email=body.email.lower()).first()
    if not u or not auth.verify_password(body.password, u.password_hash) or u.role != "ADMIN":
        raise HTTPException(401, "Invalid admin credentials")
    return {"ok": True, "data": {"token": auth.make_token(u), "role": u.role, "name": u.name}}
