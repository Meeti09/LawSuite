"""Seed: admin, users, 10 lawyers (1 pending Ananya Mehta), sources, matters. Clearly demo."""
from .database import SessionLocal, engine, Base
from . import models, auth
from .rag.seed_sources import SEED_SOURCES

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(models.User).count() > 0:
        print("Seed skipped: data exists"); return
    admin = models.User(name="Admin", email="admin@lawsuite.in", password_hash=auth.hash_password("Admin@123"), role="ADMIN")
    user = models.User(name="Demo Citizen", email="user@lawsuite.in", password_hash=auth.hash_password("User@123"), role="USER", city="Mumbai", state="Maharashtra")
    db.add_all([admin, user]); db.flush()
    for s in SEED_SOURCES:
        db.add(models.LegalSource(source_name=s["source_name"] + " [DEMO]", source_url=s["source_url"], title=s["title"],
                                  act=s["act"], section=s["section"], year=s["year"], jurisdiction=s["jurisdiction"],
                                  category=s["category"], content=s["content"], simple_explanation=s["simple_explanation"],
                                  last_verified="2026-01-01", status="ACTIVE"))
    demo_lawyers = [
        ("Adv. Ananya Mehta", "ananya.mehta@demo.in", "MH/12345/2018", "Mumbai", "Maharashtra", 8, ["Property Law", "Civil Law"], ["en", "hi", "mr"], "PENDING"),
        ("Adv. Rohan Desai", "rohan.desai@demo.in", "MH/22231/2015", "Pune", "Maharashtra", 11, ["Employment Law", "Labour Law"], ["en", "mr", "hi"], "VERIFIED"),
        ("Adv. Priya Nair", "priya.nair@demo.in", "KL/98765/2016", "Kochi", "Kerala", 9, ["Family Law", "Women & Child Rights"], ["en", "hi"], "VERIFIED"),
        ("Adv. Arjun Reddy", "arjun.reddy@demo.in", "AP/45678/2019", "Hyderabad", "Telangana", 6, ["Corporate Law", "Startup & Business Law"], ["en", "te"], "VERIFIED"),
        ("Adv. Kavya Iyer", "kavya.iyer@demo.in", "TN/11223/2017", "Chennai", "Tamil Nadu", 9, ["Consumer Law", "Civil Law"], ["en", "ta"], "VERIFIED"),
        ("Adv. Vikram Singh", "vikram.singh@demo.in", "DL/33445/2012", "New Delhi", "Delhi", 14, ["Criminal Law", "Cyber Law"], ["en", "hi"], "VERIFIED"),
        ("Adv. Sneha Kulkarni", "sneha.k@demo.in", "MH/77889/2020", "Nagpur", "Maharashtra", 5, ["Tax Law", "Banking & Finance"], ["en", "mr"], "VERIFIED"),
        ("Adv. Farhan Qureshi", "farhan.q@demo.in", "GJ/99001/2014", "Ahmedabad", "Gujarat", 12, ["Intellectual Property", "Corporate Law"], ["en", "gu", "hi"], "VERIFIED"),
        ("Adv. Divya Rao", "divya.rao@demo.in", "KA/55667/2018", "Bengaluru", "Karnataka", 7, ["Cyber Law", "Consumer Law"], ["en", "kn"], "VERIFIED"),
        ("Adv. Sourav Banerjee", "sourav.b@demo.in", "WB/44332/2013", "Kolkata", "West Bengal", 13, ["Immigration", "Civil Law"], ["en", "bn", "hi"], "VERIFIED"),
    ]
    import re
    for name, email, enroll, city, state, exp, pas, langs, status in demo_lawyers:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + "-" + enroll.lower().replace("/", "-")
        l = models.Lawyer(slug=slug, full_name=name, email=email, city=city, state=state, enrollment_number=enroll,
                          experience_years=exp, bio=f"{name} practices {', '.join(pas)} with {exp} years of experience. [DEMO PROFILE]",
                          courts=["District Court", "High Court"], verification_status=status, rating=4.5)
        db.add(l); db.flush()
        for pa in pas: db.add(models.LawyerPracticeArea(lawyer_id=l.id, practice_area=pa))
        for lg in langs: db.add(models.LawyerLanguage(lawyer_id=l.id, language=lg))
        db.add(models.LawyerVerification(lawyer_id=l.id, document_type="enrollment_certificate", document_url="demo://certificate.pdf", status=status))
    db.commit()
    print("Seeded demo data. Admin: admin@lawsuite.in / Admin@123")

if __name__ == "__main__":
    run()
