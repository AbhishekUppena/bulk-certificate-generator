from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.schemas import JobCreate
from app.crud import create_job
from app.models import Job, Certificate
from app.services.job_service import process_job


router = APIRouter(
    prefix="/api",
    tags=["Jobs"]
)


def run_job_in_background(job_id: int):
    db = SessionLocal()

    try:
        process_job(job_id, db)
    finally:
        db.close()


@router.post("/jobs/")
def create_certificate_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = create_job(db, job_data)

    background_tasks.add_task(
        run_job_in_background,
        job.id
    )

    return {
        "job_id": job.id,
        "status": "PENDING",
        "total_recipients": job.total_recipients,
        "message": "Certificate generation job created successfully"
    }


@router.get("/jobs/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    processed_count = (
        job.successful_count + job.failed_count
    )

    progress_percentage = 0

    if job.total_recipients > 0:
        progress_percentage = round(
            (processed_count / job.total_recipients) * 100,
            2
        )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "processed_count": processed_count,
        "successful_count": job.successful_count,
        "failed_count": job.failed_count,
        "progress_percentage": progress_percentage
    }


@router.get("/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    file_path = Path(certificate.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=file_path.name
    )