from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_job_status():
    payload = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Status User",
                "email": "statususer@gmail.com"
            }
        ]
    }

    create_response = client.post("/api/jobs/", json=payload)

    assert create_response.status_code == 200

    job_id = create_response.json()["job_id"]

    status_response = client.get(f"/api/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert "status" in data
    assert "total_recipients" in data
    assert "processed_count" in data
    assert "successful_count" in data
    assert "failed_count" in data
    assert "progress_percentage" in data