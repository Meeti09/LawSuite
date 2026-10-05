"""Password hashing (PBKDF2, no native deps), JWT sessions, server-side RBAC."""
import hashlib, hmac, os, base64, time
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings
from . import models

bearer = HTTPBearer(auto_error=False)


def hash_password(pw: str) -> str:
    salt = base64.b64encode(os.urandom(16)).decode()
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 120_000)
    return f"pbkdf2${salt}${base64.b64encode(dk).decode()}"


def verify_password(pw: str, h: str) -> bool:
    try:
        _, salt, dig = h.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 120_000)
        return hmac.compare_digest(base64.b64encode(dk).decode(), dig)
    except Exception:
        return False


def make_token(user) -> str:
    now = int(time.time())
    payload = {"sub": user.id, "role": user.role, "email": user.email,
               "iat": now, "exp": now + settings.JWT_EXPIRE_MINUTES * 60}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if not creds:
        raise HTTPException(401, "Not authenticated")
    try:
        p = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except Exception:
        raise HTTPException(401, "Invalid or expired session")
    u = db.query(models.User).filter_by(id=p.get("sub")).first()
    if not u:
        raise HTTPException(401, "User not found")
    return u


def require_roles(*roles):
    def _check(u=Depends(current_user)):
        if u.role not in roles:
            raise HTTPException(403, "Forbidden for role " + u.role)
        return u
    return _check


def audit(db: Session, actor_id, actor_role, action, entity=None, entity_id=None, detail=None):
    db.add(models.AuditLog(actor_id=actor_id, actor_role=actor_role, action=action,
                           entity=entity, entity_id=entity_id, detail=detail))
    db.commit()
