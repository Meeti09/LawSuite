"""LLM abstraction: demo rule-based provider + OpenAI-compatible provider. Never fabricate citations."""
import os, re
from ..config import settings

DISCLAIMER = "AI-generated information is for general informational purposes and is not a substitute for advice from a qualified legal professional."
HIGH_RISK = ["arrest", "fir", "domestic violence", "dowry", "pocso", "rape", "murder", "evict", "deadline", "notice", "lawsuit", "court", "police", "custody"]

CATEGORY_KEYWORDS = {
    "Property Law": ["rent", "deposit", "landlord", "tenant", "property", "evict", "lease", "flat", "house"],
    "Employment Law": ["salary", "employer", "job", "fired", "terminat", "offer letter", "pf", "gratuity", "workplace"],
    "Consumer Law": ["refund", "consumer", "product", "defect", "warranty", "seller", "flipkart", "amazon", "shop"],
    "Family Law": ["divorce", "marriage", "custody", "maintenance", "dowry", "alimony"],
    "Criminal Law": ["fir", "police", "arrest", "theft", "fraud", "cheat", "threat"],
    "Cyber Law": ["otp", "upi", "phishing", "hack", "online fraud", "whatsapp scam"],
    "Women & Child Rights": ["harassment", "posh", "domestic violence", "pocso", "dowry"],
    "Labour Law": ["wages", "contract labour", "esi", "bonus"],
    "Banking & Finance": ["loan", "emi", "bank", "cheque bounce", "138"],
    "Tax Law": ["gst", "income tax", "notice", "tds"],
}

FOLLOW_UPS = {
    "Property Law": ["Which state is the property located in?", "Do you have a written rental agreement?", "When did you vacate / when was rent due?"],
    "Employment Law": ["Which state do you work in?", "Do you have a written employment agreement or offer letter?", "How long has the salary been unpaid?"],
    "Consumer Law": ["What did you purchase and when?", "Do you have the bill / invoice?", "Have you contacted the seller in writing?"],
    "Family Law": ["Which city/state are you in?", "Is there a written agreement or court case already?", "Are there children involved?"],
    "Criminal Law": ["Which city/state did this happen in?", "Have you approached the police yet?", "Do you have any written evidence (messages, receipts)?"],
    "Cyber Law": ["What amount is involved, if any?", "Do you have transaction IDs / screenshots?", "Have you reported on cybercrime.gov.in or 1930?"],
}


def detect_category(text: str) -> str:
    t = text.lower()
    best, score = "General", 0
    for cat, kws in CATEGORY_KEYWORDS.items():
        s = sum(1 for k in kws if k in t)
        if s > score:
            best, score = cat, s
    return best


def is_high_risk(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in HIGH_RISK)


class LLMProvider:
    def complete(self, messages, **kw) -> str:
        raise NotImplementedError


class DemoLLMProvider(LLMProvider):
    """Deterministic guided-intake engine: no external API, safe language, progressive questions."""
    def complete(self, messages, **kw) -> str:
        last = messages[-1]["content"] if messages else ""
        cat = detect_category(" ".join(m["content"] for m in messages))
        risk = is_high_risk(last)
        qs = FOLLOW_UPS.get(cat, ["Which state/city did this happen in?", "Do you have any documents related to this?"])
        answered = len([m for m in messages if m["role"] == "user"])
        out = f"Based on the information provided, this looks like it may relate to **{cat}**. "
        if risk:
            out += "This situation may require professional legal assistance. Consider connecting with a qualified lawyer. "
        if answered < 3:
            out += f"\n\nTo help you better: {qs[min(answered-1, len(qs)-1)]}"
        else:
            out += ("\n\n**What we understood (preliminary):** your description has been noted. "
                    "\n**Possible next steps:** 1) Preserve records & messages 2) Review any written agreement "
                    "3) Send a written request 4) Consider professional legal advice. " + DISCLAIMER)
        return out


class OpenAICompatibleProvider(LLMProvider):
    def complete(self, messages, **kw) -> str:
        # Lazy import; falls back to demo if unavailable
        try:
            from openai import OpenAI
            c = OpenAI(api_key=settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"))
            r = c.chat.completions.create(model=settings.OPENAI_MODEL, messages=messages)
            return r.choices[0].message.content
        except Exception as e:
            return DemoLLMProvider().complete(messages) + f"\n\n(LLM fallback: {e})"


def get_llm() -> LLMProvider:
    if settings.LLM_PROVIDER == "openai" and (settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")):
        return OpenAICompatibleProvider()
    return DemoLLMProvider()
