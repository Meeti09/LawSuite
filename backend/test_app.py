from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)

def test_health(): assert c.get("/api/health").json()["ok"]
def test_register_login():
    r = c.post("/api/auth/register", json={"name": "T User", "email": "t@t.in", "password": "secret123"})
    assert r.status_code in (200, 400)
def test_chat_grounded():
    r = c.post("/api/legal-help/chat", json={"message": "landlord not returning deposit"})
    assert r.json()["ok"] and "brief" in r.json()["data"]
def test_research_no_fabrication():
    r = c.post("/api/legal-research/search", json={"query": "zzzz unknown xyz"})
    assert "couldn't find" in r.json()["data"]["answer"].lower()
def test_whatsapp_simulate():
    r = c.post("/api/whatsapp/simulate", json={"phone": "919999999999", "message": "Hi"})
    assert r.json()["ok"]
def test_admin_forbidden():
    assert c.get("/api/admin/overview").status_code in (401, 403)
