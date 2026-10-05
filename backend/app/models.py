"""All core tables: users, lawyers, matters, docs, RAG, WhatsApp, admin. UUIDs + timestamps + indexes."""
import uuid, datetime
from sqlalchemy import (Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Float, JSON, Index, UniqueConstraint)
from .database import Base


def _uuid():
    return str(uuid.uuid4())


def _now():
    return datetime.datetime.utcnow()


class TimestampMixin:
    created_at = Column(DateTime, default=_now, nullable=False)
    updated_at = Column(DateTime, default=_now, onupdate=_now, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String(200), nullable=False)
    email = Column(String(320), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True, index=True)
    password_hash = Column(String(300), nullable=False)
    role = Column(String(20), default="USER", nullable=False)  # USER | LAWYER | ADMIN
    preferred_language = Column(String(10), default="en")
    city = Column(String(120), nullable=True)
    state = Column(String(120), nullable=True)


class Lawyer(Base, TimestampMixin):
    __tablename__ = "lawyers"
    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    photo_url = Column(String(500), nullable=True)
    email = Column(String(320), nullable=False)
    phone = Column(String(30), nullable=True, index=True)
    city = Column(String(120), nullable=True, index=True)
    state = Column(String(120), nullable=True, index=True)
    enrollment_number = Column(String(100), nullable=False)
    experience_years = Column(Integer, default=0)
    firm = Column(String(220), nullable=True)
    bio = Column(Text, nullable=True)
    courts = Column(JSON, default=list)
    availability = Column(String(100), default="Available")
    verification_status = Column(String(30), default="PENDING", index=True)  # PENDING|VERIFIED|REJECTED|SUSPENDED
    verification_notes = Column(Text, nullable=True)
    rating = Column(Float, default=0)
    consultations_count = Column(Integer, default=0)


class LawyerPracticeArea(Base):
    __tablename__ = "lawyer_practice_areas"
    id = Column(String, primary_key=True, default=_uuid)
    lawyer_id = Column(String, ForeignKey("lawyers.id"), nullable=False, index=True)
    practice_area = Column(String(120), nullable=False, index=True)


class LawyerLanguage(Base):
    __tablename__ = "lawyer_languages"
    id = Column(String, primary_key=True, default=_uuid)
    lawyer_id = Column(String, ForeignKey("lawyers.id"), nullable=False, index=True)
    language = Column(String(20), nullable=False, index=True)


class LawyerVerification(Base, TimestampMixin):
    __tablename__ = "lawyer_verifications"
    id = Column(String, primary_key=True, default=_uuid)
    lawyer_id = Column(String, ForeignKey("lawyers.id"), nullable=False, index=True)
    document_type = Column(String(100), nullable=False)
    document_url = Column(String(500), nullable=False)
    status = Column(String(30), default="PENDING")


class LegalMatter(Base, TimestampMixin):
    __tablename__ = "legal_matters"
    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String(300), nullable=False)
    category = Column(String(120), nullable=True, index=True)
    language = Column(String(10), default="en")
    state = Column(String(120), nullable=True)
    status = Column(String(40), default="Understanding", index=True)
    summary = Column(JSON, default=dict)
    handoff_token = Column(String(64), nullable=True, unique=True)


class MatterMessage(Base):
    __tablename__ = "matter_messages"
    id = Column(String, primary_key=True, default=_uuid)
    matter_id = Column(String, ForeignKey("legal_matters.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_now)


class LawyerRequest(Base, TimestampMixin):
    __tablename__ = "lawyer_requests"
    id = Column(String, primary_key=True, default=_uuid)
    matter_id = Column(String, ForeignKey("legal_matters.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    lawyer_id = Column(String, ForeignKey("lawyers.id"), nullable=False, index=True)
    issue_summary = Column(Text, nullable=True)
    status = Column(String(30), default="PENDING", index=True)  # PENDING|ACCEPTED|REJECTED|COMPLETED


class GeneratedDocument(Base, TimestampMixin):
    __tablename__ = "generated_documents"
    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    matter_id = Column(String, ForeignKey("legal_matters.id"), nullable=True)
    doc_type = Column(String(120), nullable=False)
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(30), default="READY")


class LegalSource(Base, TimestampMixin):
    __tablename__ = "legal_sources"
    id = Column(String, primary_key=True, default=_uuid)
    source_name = Column(String(200), nullable=False)
    source_url = Column(String(600), nullable=True)
    title = Column(String(300), nullable=False)
    act = Column(String(200), nullable=True, index=True)
    section = Column(String(100), nullable=True)
    jurisdiction = Column(String(100), default="India")
    year = Column(Integer, nullable=True)
    effective_date = Column(String(30), nullable=True)
    last_verified = Column(String(30), nullable=True)
    content = Column(Text, nullable=False)
    simple_explanation = Column(Text, nullable=True)
    category = Column(String(120), nullable=True, index=True)
    status = Column(String(20), default="ACTIVE")


class AIConversation(Base, TimestampMixin):
    __tablename__ = "ai_conversations"
    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    language = Column(String(10), default="en")
    category = Column(String(120), nullable=True, index=True)
    escalated = Column(Boolean, default=False)
    feedback = Column(String(20), nullable=True)


class WhatsAppConversation(Base, TimestampMixin):
    __tablename__ = "whatsapp_conversations"
    id = Column(String, primary_key=True, default=_uuid)
    phone = Column(String(30), nullable=False, index=True)
    language = Column(String(10), default="en")
    state = Column(String(40), default="START")
    category = Column(String(120), nullable=True)
    facts = Column(JSON, default=dict)
    status = Column(String(30), default="AI_HANDLING", index=True)
    handoff_token = Column(String(64), nullable=True, unique=True)


class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"
    id = Column(String, primary_key=True, default=_uuid)
    conversation_id = Column(String, ForeignKey("whatsapp_conversations.id"), nullable=False, index=True)
    direction = Column(String(10), nullable=False)  # IN | OUT
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_now)


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    kind = Column(String(80), nullable=False)
    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=True)
    read = Column(Boolean, default=False)


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, default=_uuid)
    lawyer_id = Column(String, ForeignKey("lawyers.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=_uuid)
    actor_id = Column(String, nullable=True)
    actor_role = Column(String(20), nullable=True)
    action = Column(String(120), nullable=False)
    entity = Column(String(120), nullable=True)
    entity_id = Column(String(100), nullable=True)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now)

Index("ix_users_email_lower", User.email)
