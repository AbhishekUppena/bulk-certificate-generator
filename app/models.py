from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String(255), nullable=False)
    event_date = Column(String(50), nullable=False)

    status = Column(String(50), default="PENDING", nullable=False)

    total_recipients = Column(Integer, default=0)
    successful_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    status = Column(String(50), default="PENDING", nullable=False)
    error_message = Column(String(500), nullable=True)

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    job = relationship(
        "Job",
        back_populates="recipients"
    )

    certificate = relationship(
        "Certificate",
        back_populates="recipient",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    file_path = Column(String(500), nullable=False)
    status = Column(String(50), default="GENERATED", nullable=False)

    recipient_id = Column(
        Integer,
        ForeignKey("recipients.id"),
        nullable=False,
        unique=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    recipient = relationship(
        "Recipient",
        back_populates="certificate"
    )