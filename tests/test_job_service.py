from app.services import job_service


def test_one_certificate_failure_does_not_stop_others(monkeypatch):
    calls = []

    def fake_generate_certificate(
        recipient_name,
        event_name,
        event_date,
        certificate_id
    ):
        calls.append(recipient_name)

        if recipient_name == "Bad User":
            raise Exception("Simulated certificate generation failure")

        return f"certificates/test_{certificate_id}.pdf"

    monkeypatch.setattr(
        job_service,
        "generate_certificate",
        fake_generate_certificate
    )

    assert fake_generate_certificate(
        "Good User",
        "Test Event",
        "2026-10-07",
        1
    )

    try:
        fake_generate_certificate(
            "Bad User",
            "Test Event",
            "2026-10-07",
            2
        )
    except Exception:
        pass

    assert fake_generate_certificate(
        "Another Good User",
        "Test Event",
        "2026-10-07",
        3
    )

    assert calls == [
        "Good User",
        "Bad User",
        "Another Good User"
    ]