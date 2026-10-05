"""Document templates: guided Q&A -> draft. Every draft carries review disclaimer."""
DISCLAIMER = "Template generated from the information provided. Review with a qualified legal professional when appropriate."

TEMPLATES = {
    "legal_notice": {"title": "Legal Notice", "fields": ["sender_name", "recipient_name", "facts", "demand", "deadline_days", "city", "date"]},
    "rental_agreement": {"title": "Rental Agreement (draft)", "fields": ["landlord", "tenant", "property_address", "rent", "deposit", "tenure_months", "city"]},
    "consumer_complaint": {"title": "Consumer Complaint (draft)", "fields": ["complainant", "opposite_party", "product", "purchase_date", "amount", "grievance", "relief"]},
    "nda": {"title": "Non-Disclosure Agreement (draft)", "fields": ["party_a", "party_b", "purpose", "tenure_months", "city"]},
    "rti": {"title": "RTI Application", "fields": ["applicant_name", "address", "pio_office", "information_sought", "date"]},
    "complaint_letter": {"title": "Complaint Letter", "fields": ["sender", "recipient", "subject", "facts", "request"]},
    "affidavit": {"title": "Affidavit Template", "fields": ["deponent", "address", "statements", "city", "date"]},
    "employment_letter": {"title": "Employment Demand Letter", "fields": ["employee", "employer", "dues", "period", "city", "date"]},
    "partnership": {"title": "Partnership Agreement (draft)", "fields": ["partner_a", "partner_b", "business", "capital_a", "capital_b", "city"]},
}


def render(doc_type: str, fields: dict) -> str:
    t = TEMPLATES.get(doc_type, {"title": doc_type})
    lines = [t["title"].upper(), "=" * 40, ""]
    for k in t.get("fields", []):
        lines.append(f"{k.replace('_',' ').title()}: {fields.get(k, '________')}")
    lines += ["", "Statement:", fields.get("facts", fields.get("grievance", fields.get("information_sought", "As described by the user."))), "", DISCLAIMER]
    return "\n".join(lines)
