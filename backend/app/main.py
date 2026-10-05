from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from . import models  # noqa: ensure tables registered
from .api import auth, legal_help, research, documents, lawyers, matters, whatsapp, admin

Base.metadata.create_all(bind=engine)
app = FastAPI(title="LawSuite API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS.split(","),
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

for r in (auth.router, legal_help.router, research.router, documents.router, lawyers.router, matters.router, whatsapp.router, admin.router):
    app.include_router(r)


@app.get("/api/health")
def health():
    return {"ok": True, "data": {"service": "lawsuite-backend", "demo": settings.DEMO_MODE}}
