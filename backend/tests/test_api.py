import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_plan_missing_fields_returns_422():
    response = client.post("/plan", json={})
    assert response.status_code == 422

@pytest.mark.skip(reason="Skipping full pipeline test - uses Groq tokens")
def test_plan_invalid_travel_mode():
    response = client.post("/plan", json={
        "from_city": "Delhi",
        "destination": "Manali",
        "start_date": "2026-12-20",
        "end_date": "2026-12-25",
        "budget": 30000,
        "group_size": 2,
        "travel_mode": "helicopter",  # invalid
        "preferences": []
    })
    assert response.status_code in [400, 422]

@pytest.mark.skip(reason="Skipping full pipeline test - uses Groq tokens")
def test_plan_end_before_start_returns_error():
    response = client.post("/plan", json={
        "from_city": "Delhi",
        "destination": "Manali",
        "start_date": "2026-12-25",
        "end_date": "2026-12-20",  # end before start
        "budget": 30000,
        "group_size": 2,
        "travel_mode": "train",
        "preferences": []
    })
    assert response.status_code in [400, 422]