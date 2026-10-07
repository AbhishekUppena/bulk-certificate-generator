# Bulk Certificate Generator API

A FastAPI backend for generating participation certificates in bulk.

The API accepts a list of recipients, creates a certificate-generation job, processes certificates in the background, tracks job progress, and provides generated certificates for download.

## Features

- Bulk certificate generation
- Recipient input validation
- Background certificate processing
- PDF certificate generation using ReportLab
- Job status tracking
- Processing progress percentage
- Successful and failed certificate counts
- Individual certificate retrieval
- Failure isolation between recipients
- SQLite relational database
- Automated tests using Pytest
- Interactive API documentation using Swagger UI

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- Uvicorn

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── certificate_service.py
│   │   └── job_service.py
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── certificates/
│
├── tests/
│   ├── test_api.py
│   ├── test_certificate_service.py
│   └── test_job_service.py
│
├── .gitignore
├── README.md
└── requirements.txt