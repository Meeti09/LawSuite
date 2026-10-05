"""Lightweight RAG: TF-IDF-ish scoring over seeded LegalSources. No fabricated citations."""
import re
from collections import Counter

TOKEN = re.compile(r"[a-zA-Z\u0900-\u097F]+")


def tokens(s: str):
    return [t.lower() for t in TOKEN.findall(s or "")]


def score(query: str, doc_text: str) -> float:
    q, d = Counter(tokens(query)), Counter(tokens(doc_text))
    if not q:
        return 0.0
    overlap = sum(min(q[t], d.get(t, 0)) for t in q)
    return overlap / max(1, len(tokens(query)))


def retrieve(query: str, sources: list, filters: dict | None = None, top_k: int = 5):
    f = filters or {}
    cands = []
    for s in sources:
        if f.get("act") and f["act"].lower() not in (s.act or "").lower():
            continue
        if f.get("category") and f["category"].lower() not in (s.category or "").lower():
            continue
        if f.get("year") and s.year != int(f["year"]):
            continue
        sc = score(query, f"{s.title} {s.act} {s.section} {s.content} {s.category}")
        if sc > 0:
            cands.append((sc, s))
    cands.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in cands[:top_k]]


def grounded_answer(query: str, docs: list) -> dict:
    if not docs:
        return {"answer": "I couldn't find enough reliable information to answer this confidently.", "citations": []}
    lines = [f"Based on the information provided, here is general information related to your query."]
    cites = []
    for d in docs:
        lines.append(f"- {d.title} ({d.act or ''} {d.section or ''}): {d.simple_explanation or d.content[:220]}")
        cites.append({"id": d.id, "title": d.title, "act": d.act, "section": d.section,
                      "source_name": d.source_name, "source_url": d.source_url})
    lines.append("AI-generated information is for general informational purposes and is not a substitute for advice from a qualified legal professional.")
    return {"answer": "\n".join(lines), "citations": cites}
