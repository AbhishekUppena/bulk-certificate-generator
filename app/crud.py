from sqlalchemy.orm import Session

from app.models import Job, Recipient
from app.schemas import JobCreate


def create_job(db: Session, job_data: JobCreate):
    job = Job(
        event_name=job_data.event_name,
        event_date=job_data.event_date,
        status="PENDING",
        total_recipients=len(job_data.recipients),
        successful_count=0,
        failed_count=0,
    )

    db.add(job)
    db.flush()

    for recipient_data in job_data.recipients:
        recipient = Recipient(
            name=recipient_data.name,
            email=recipient_data.email,
            status="PENDING",
            job_id=job.id,
        )

        db.add(recipient)

    db.commit()
    db.refresh(job)

    return job