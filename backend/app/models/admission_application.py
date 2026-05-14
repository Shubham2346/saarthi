"""
Structured college admission application draft, co-filled by the agentic assistant.
One row per user (upsert pattern).
"""

import uuid
from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User


class AdmissionApplication(SQLModel, table=True):
    __tablename__ = "admission_applications"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True, index=True)

    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=32)
    date_of_birth: Optional[date] = Field(default=None)

    address_line1: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=120)
    state: Optional[str] = Field(default=None, max_length=120)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    country: Optional[str] = Field(default=None, max_length=120)

    program_choice: Optional[str] = Field(default=None, max_length=255)
    previous_institution: Optional[str] = Field(default=None, max_length=255)
    board_10: Optional[str] = Field(default=None, max_length=64)
    percentage_10: Optional[str] = Field(default=None, max_length=32)
    board_12: Optional[str] = Field(default=None, max_length=64)
    percentage_12: Optional[str] = Field(default=None, max_length=32)

    guardian_name: Optional[str] = Field(default=None, max_length=255)
    guardian_phone: Optional[str] = Field(default=None, max_length=32)
    extracurriculars: Optional[str] = Field(default=None, max_length=2000)
    statement_of_purpose: Optional[str] = Field(default=None, max_length=4000)

    pipeline_percent: int = Field(default=0, ge=0, le=100)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(
        back_populates="admission_application",
        sa_relationship_kwargs={"foreign_keys": "[AdmissionApplication.user_id]"},
    )
