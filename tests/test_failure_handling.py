from app.crud import create_job
from app.database import SessionLocal
from app.models import Job, Recipient
from app.schemas import JobCreate, RecipientCreate
from app.services import job_service


def test_failure_handling(monkeypatch):
    db = SessionLocal()

    try:
        job_data = JobCreate(
            event_name="Failure Handling Test",
            event_date="2026-10-07",
            recipients=[
                RecipientCreate(
                    name="Good User",
                    email="good@gmail.com"
                ),
                RecipientCreate(
                    name="Bad User",
                    email="bad@gmail.com"
                ),
                RecipientCreate(
                    name="Another Good User",
                    email="another@gmail.com"
                )
            ]
        )

        job = create_job(db, job_data)
        job_id = job.id

        def fake_generate_certificate(
            recipient_name,
            event_name,
            event_date,
            certificate_id
        ):
            if recipient_name == "Bad User":
                raise Exception("Simulated certificate failure")

            return f"certificates/test_{certificate_id}.pdf"

        monkeypatch.setattr(
            job_service,
            "generate_certificate",
            fake_generate_certificate
        )

        job_service.process_job(job_id, db)

        updated_job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job_id)
            .all()
        )

        assert updated_job is not None
        assert updated_job.successful_count == 2
        assert updated_job.failed_count == 1
        assert updated_job.status == "COMPLETED_WITH_ERRORS"

        statuses = {
            recipient.name: recipient.status
            for recipient in recipients
        }

        assert statuses["Good User"] == "SUCCESS"
        assert statuses["Bad User"] == "FAILED"
        assert statuses["Another Good User"] == "SUCCESS"

    finally:
        db.close()