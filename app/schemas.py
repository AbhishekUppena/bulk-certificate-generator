from pydantic import BaseModel, EmailStr, Field
from typing import List


class RecipientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr


class JobCreate(BaseModel):
    event_name: str = Field(..., min_length=2, max_length=255)
    event_date: str
    recipients: List[RecipientCreate] = Field(..., min_length=1)