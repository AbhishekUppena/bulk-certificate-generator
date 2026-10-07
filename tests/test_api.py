from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_job():
    payload = {
        "event_name": "Test Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Rahul Kumar",
                "email": "rahul@gmail.com"
            },
            {
                "name": "Priya Sharma",
                "email": "priya@gmail.com"
            }
        ]
    }

    response = client.post("/api/jobs/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total_recipients"] == 2


def test_invalid_recipient():
    payload = {
        "event_name": "Test Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "",
                "email": "invalid-email"
            }
        ]
    }

    response = client.post("/api/jobs/", json=payload)

    assert response.status_code == 422