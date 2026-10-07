from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Certificate

client = TestClient(app)


def test_certificate_retrieval():
    payload = {
        "event_name": "Certificate Retrieval Test",
        "event_date": "2026-10-07",
        "recipients": [
            {
                "name": "Retrieval User",
                "email": "retrieval@gmail.com"
            }
        ]
    }

    create_response = client.post("/api/jobs/", json=payload)

    assert create_response.status_code == 200

    db = SessionLocal()

    try:
        certificate = db.query(Certificate).order_by(
            Certificate.id.desc()
        ).first()

        assert certificate is not None

        certificate_id = certificate.id

    finally:
        db.close()

    response = client.get(
        f"/api/certificates/{certificate_id}"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"