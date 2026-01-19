import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Remove if already present (allow 404 or 200)
    pre_unreg = client.post("/unregister", json={"activity": activity, "email": email})
    assert pre_unreg.status_code in (200, 404)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post("/unregister", json={"activity": activity, "email": email})
    assert response_unreg.status_code in (200, 404)
    if response_unreg.status_code == 200:
        assert "Removed" in response_unreg.json()["message"]

def test_signup_invalid_activity():
    response = client.post("/activities/invalid_activity/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unreg_invalid_participant():
    activity = list(client.get("/activities").json().keys())[0]
    response = client.post("/unregister", json={"activity": activity, "email": "notfound@mergington.edu"})
    assert response.status_code == 404
