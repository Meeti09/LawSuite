# LawSuite — Legal help, made understandable.

Accessible LegalTech for India: guided AI intake (8 languages) + WhatsApp + grounded research + documents + verified lawyers. Original brand, UI, copy and code (conceptually inspired by the LegalTech problem space, not a clone).

## Quick demo (no Docker)
### Backend
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate
pip install -r requirements.txt
copy .env.example .env
python seed_demo.py        # creates SQLite DB + admin/user/10 lawyers/sources
python -m uvicorn app.main:app --reload --port 8000
```
Admin: `admin@lawsuite.in / Admin@123` · User: `user@lawsuite.in / User@123`
Pending-demo lawyer: **Adv. Ananya Mehta** → approve at `/admin` → appears on `/lawyers`.

PostgreSQL (production): set `DATABASE_URL=postgresql+psycopg2://...`, install `psycopg2-binary`, same seed command. Redis/Chroma are optional extensions (in-memory + SQL retrieval ship the demo).

### Frontend
```powershell
cd frontend
copy .env.example .env.local
npm install
npm run dev   # http://localhost:3000
```

## Judge flow (2 min)
1. Home → **Describe My Legal Problem** → type landlord/deposit issue → guided questions → category + next steps.
2. **Documents** → Consumer Complaint → generate → print/PDF.
3. **Find a Lawyer** → open verified profile → Request Consultation.
4. **Sign In** as admin → **Admin** → Approve *Ananya Mehta* → she appears in directory (audit logged).
5. **Talk on WhatsApp** (wa.me link) or **Try mock demo** → multilingual state machine → handoff token → continue on web.
6. **Legal Research** → grounded answer with citations; unknown queries honestly say "couldn't find enough reliable information".

## Architecture
`FastAPI + SQLAlchemy + PBKDF2/JWT + RBAC (server-enforced)` · `LLMProvider` (demo rule engine / OpenAI-compatible via `LLM_PROVIDER`) · lightweight TF-IDF RAG (Chroma-ready) · `WhatsAppProvider` (mock / Cloud stub) + `wa.me` fallback · `PaymentProvider`-ready consultation (no charge in demo).
DB tables: users, lawyers, lawyer_verifications, practice areas, languages, matters, matter_messages, documents, lawyer_requests, legal_sources, ai_conversations, whatsapp_*, notifications, reviews, audit_logs — UUIDs, FKs, timestamps, indexes.
Safety: general-information disclaimer everywhere, high-risk escalation ("may require professional legal assistance"), no fabricated citations, masked phone numbers in admin, handoff tokens (never sensitive data in URLs).

## Security / Privacy
Hashed passwords, JWT expiry, role checks server-side, input validation (Pydantic), upload validation stubs, CORS allowlist, audit logs, download/delete affordances. Never commit `.env`.

## Tests
```powershell
cd backend; pytest -q
```
Covers auth, RBAC denial, intake, RAG honesty, doc-gen validation, WhatsApp state, verification flow.
