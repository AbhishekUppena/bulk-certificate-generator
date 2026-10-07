from pathlib import Path

from app.services.certificate_service import generate_certificate


def test_generate_certificate():
    file_path = generate_certificate(
        recipient_name="Test User",
        event_name="Python Workshop",
        event_date="2026-10-07",
        certificate_id=9999
    )

    assert Path(file_path).exists()
    assert file_path.endswith(".pdf")

    # Clean up test file
    Path(file_path).unlink()