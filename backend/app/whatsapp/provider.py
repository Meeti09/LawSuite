"""WhatsApp provider abstraction: Mock + Meta Cloud stub. wa.me deep link keeps CTA functional."""
import httpx
from ..config import settings


class WhatsAppProvider:
    def send_message(self, to: str, body: str) -> dict: raise NotImplementedError
    def send_interactive(self, to: str, body: str, buttons: list) -> dict: raise NotImplementedError
    def mark_as_read(self, message_id: str) -> dict: return {"ok": True}


class MockWhatsAppProvider(WhatsAppProvider):
    SENT: list = []
    def send_message(self, to, body):
        self.SENT.append({"to": to, "body": body})
        return {"ok": True, "provider": "mock", "to": to}
    def send_interactive(self, to, body, buttons):
        self.SENT.append({"to": to, "body": body, "buttons": buttons})
        return {"ok": True, "provider": "mock"}


class CloudWhatsAppProvider(WhatsAppProvider):
    def send_message(self, to, body):
        if not settings.WHATSAPP_CLOUD_TOKEN or not settings.WHATSAPP_PHONE_NUMBER_ID:
            return MockWhatsAppProvider().send_message(to, body)
        url = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        r = httpx.post(url, headers={"Authorization": f"Bearer {settings.WHATSAPP_CLOUD_TOKEN}"},
                       json={"messaging_product": "whatsapp", "to": to, "text": {"body": body}}, timeout=15)
        return {"ok": r.status_code < 300, "status": r.status_code}


def get_whatsapp() -> WhatsAppProvider:
    if settings.WHATSAPP_PROVIDER == "cloud":
        return CloudWhatsAppProvider()
    return MockWhatsAppProvider()


STATES = ["START", "LANGUAGE_SELECTION", "ISSUE_DESCRIPTION", "FOLLOW_UP", "LEGAL_CLASSIFICATION", "GUIDANCE", "DOCUMENT_OPTION", "LAWYER_OPTION", "COMPLETED"]
GREETINGS = {"en": "Hello! I'm LawSuite. Describe your legal problem in your own words.", "hi": "नमस्ते! मैं LawSuite हूँ। अपनी समस्या अपने शब्दों में बताइए।", "mr": "नमस्कार! मी LawSuite आहे. तुमची समस्या तुमच्या शब्दांत सांगा."}


def next_state(current: str) -> str:
    i = STATES.index(current) if current in STATES else 0
    return STATES[min(i + 1, len(STATES) - 1)]
