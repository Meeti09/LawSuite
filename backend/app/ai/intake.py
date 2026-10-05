"""Guided legal intake: 1-2 questions at a time, progress stages, grounded next-steps, safety copy."""
from .llm_provider import get_llm, detect_category, is_high_risk, DISCLAIMER, FOLLOW_UPS

STAGES = ["Understanding your situation", "Identifying legal area", "Finding relevant information", "Preparing your next step"]
HIGH_RISK_NOTE = "This situation may require professional legal assistance. Consider connecting with a qualified lawyer."


def run_intake(history: list[dict], language: str = "en") -> dict:
    user_text = " ".join(m["content"] for m in history if m["role"] == "user")
    category = detect_category(user_text)
    risk = is_high_risk(user_text)
    llm = get_llm()
    reply = llm.complete([{"role": "m", "content": m["content"]} for m in history])
    # Never translate statute names: keep citations in English (handled in RAG layer)
    n_user = len([m for m in history if m["role"] == "user"])
    stage = STAGES[min(n_user - 1, 3)] if n_user else STAGES[0]
    brief = {
        "category": category,
        "language": language,
        "facts": [history[-1]["content"][:280]] if history else [],
        "escalate": risk,
        "next_steps": [
            "Preserve records, messages and receipts",
            "Review any written agreement",
            "Send a polite written request and keep proof",
            "Consider professional legal advice" + (" (recommended here)" if risk else ""),
        ],
        "disclaimer": DISCLAIMER,
        "high_risk_note": HIGH_RISK_NOTE if risk else None,
        "ai_label": "AI-generated preliminary summary. Verify facts directly with the client.",
    }
    return {"reply": reply, "stage": stage, "brief": brief}
