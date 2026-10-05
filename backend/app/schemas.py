"""Pydantic schemas with validation. Consistent API envelope: { ok, data, error }."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any


class Envelope(BaseModel):
    ok: bool = True
    data: Any = None
    error: Optional[str] = None


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    phone: Optional[str] = None
    role: Optional[str] = "USER"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class LawyerRegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    enrollment_number: str
    experience_years: int = 0
    practice_areas: List[str] = []
    languages: List[str] = ["en"]
    courts: List[str] = []
    firm: Optional[str] = None
    bio: Optional[str] = None
    availability: Optional[str] = "Available"
    documents: List[dict] = []


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    matter_id: Optional[str] = None
    language: Optional[str] = "en"


class ResearchIn(BaseModel):
    query: str
    act: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None


class DocGenIn(BaseModel):
    doc_type: str
    fields: dict = {}
    language: Optional[str] = "en"
    matter_id: Optional[str] = None


class LawyerRequestIn(BaseModel):
    lawyer_id: str
    matter_id: Optional[str] = None
    issue_summary: Optional[str] = None


class VerifyIn(BaseModel):
    action: str  # APPROVE | REJECT | MORE_INFO | SUSPEND
    notes: Optional[str] = None
