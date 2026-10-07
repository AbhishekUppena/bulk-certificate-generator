from pathlib import Path

from app.services.certificate_service import generate_certificate


def test_certificate_generation():
    file_path = generate_certificate(
        recipient_name="Test User",
        event_name="Python Workshop",
        event_date="2026-10-07",
        certificate_id=8888
    )

    assert Path(file_path).exists()
    assert file_path.endswith(".pdf")

    Path(file_path).unlink()