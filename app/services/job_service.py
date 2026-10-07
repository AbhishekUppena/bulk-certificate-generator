from sqlalchemy.orm import Session

from app.models import Job, Recipient, Certificate
from app.services.certificate_service import generate_certificate


def process_job(job_id: int, db: Session):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return

    job.status = "PROCESSING"
    db.commit()

    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job_id)
        .all()
    )

    successful_count = 0
    failed_count = 0

    for recipient in recipients:

        try:
            certificate = generate_certificate(
                recipient_name=recipient.name,
                event_name=job.event_name,
                event_date=job.event_date,
                certificate_id=recipient.id
            )

            recipient.status = "SUCCESS"
            recipient.error_message = None

            certificate_record = Certificate(
                file_path=certificate,
                status="GENERATED",
                recipient_id=recipient.id
            )

            db.add(certificate_record)

            successful_count += 1

        except Exception as error:

            recipient.status = "FAILED"
            recipient.error_message = str(error)

            failed_count += 1

    job.successful_count = successful_count
    job.failed_count = failed_count

    if failed_count == 0:
        job.status = "COMPLETED"
    elif successful_count == 0:
        job.status = "FAILED"
    else:
        job.status = "COMPLETED_WITH_ERRORS"

    db.commit()