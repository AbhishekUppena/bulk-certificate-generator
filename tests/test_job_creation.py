from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_job_creation():
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Test User",
                "email": "testuser@gmail.com"
            }
        ]
    }

    response = client.post("/api/jobs/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "PENDING"
    assert data["total_recipients"] == 1