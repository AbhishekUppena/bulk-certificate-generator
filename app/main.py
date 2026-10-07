from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.api.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Backend API for generating certificates in bulk",
    version="1.0.0"
)

app.include_router(router)
@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }