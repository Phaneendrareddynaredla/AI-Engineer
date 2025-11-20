import sys, os, json
sys.path.append(os.path.join(os.getcwd(), "support-triage-agent"))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_triage_endpoint_known_issue():
    payload = {"description": "Checkout keeps failing with error 500 on mobile when I try to pay."}
    r = client.post("/triage", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "summary" in j
    assert j["category"] in ["Bug","Billing","Login","Performance","Question/How-To"]
    assert j["severity"] in ["Low","Medium","High","Critical"]

def test_triage_endpoint_empty():
    r = client.post("/triage", json={"description": ""})
    assert r.status_code == 422
