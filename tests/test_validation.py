from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validation():
    payload = {
        "event_name": "Python Workshop",
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