"""Central configuration. No secrets hardcoded; all from environment."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./lawsuite.db"
    JWT_SECRET: str = "change-me-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 43200
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"
    LLM_PROVIDER: str = "demo"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    WHATSAPP_NUMBER: str = "919876543210"
    WHATSAPP_BUSINESS_URL: str = ""
    WHATSAPP_PROVIDER: str = "mock"
    WHATSAPP_VERIFY_TOKEN: str = "lawsuite-dev-verify"
    WHATSAPP_CLOUD_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    DEMO_MODE: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

WHATSAPP_DEEP_LINK = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text=Hi%20LawSuite%2C%20I%20need%20legal%20help"
SUPPORTED_LANGUAGES = [
    {"code": "en", "label": "English"},
    {"code": "hi", "label": "हिन्दी (Hindi)"},
    {"code": "mr", "label": "मराठी (Marathi)"},
    {"code": "gu", "label": "ગુજરાતી (Gujarati)"},
    {"code": "ta", "label": "தமிழ் (Tamil)"},
    {"code": "te", "label": "తెలుగు (Telugu)"},
    {"code": "bn", "label": "বাংলা (Bengali)"},
    {"code": "kn", "label": "ಕನ್ನಡ (Kannada)"},
]
PRACTICE_AREAS = [
    "Criminal Law", "Civil Law", "Family Law", "Consumer Law",
    "Property Law", "Employment Law", "Corporate Law", "Cyber Law",
    "Intellectual Property", "Tax Law", "Banking & Finance", "Immigration",
    "Labour Law", "Women & Child Rights", "Startup & Business Law",
]
