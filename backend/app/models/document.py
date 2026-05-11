"""
Document model — tracks uploaded files, OCR results, and verification status.
Used by the Document Verification Agent in later phases.
"""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import UserTask


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    VERIFIED = "verified"
    REJECTED = "rejected"


class Document(SQLModel, table=True):
    """Tracks student document uploads, OCR extraction, and admin verification."""

    __tablename__ = "documents"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    task_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user_tasks.id", index=True
    )

    # File info
    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_type: str = Field(max_length=50)  # e.g. "application/pdf", "image/jpeg"
    file_size_bytes: int = Field(default=0)

    # Verification
    status: DocumentStatus = Field(
        default=DocumentStatus.UPLOADED,
        sa_column=Column(
            SAEnum(DocumentStatus),
            nullable=False,
            default=DocumentStatus.UPLOADED,
        ),
    )
    rejection_reason: Optional[str] = Field(default=None)

    # OCR (populated by Document Verification Agent)
    ocr_text: Optional[str] = Field(default=None)
    ocr_confidence: Optional[float] = Field(default=None)

    # Admin verification
    verified_by: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    verified_at: Optional[datetime] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="documents",
        sa_relationship_kwargs={"foreign_keys": "[Document.user_id]"},
    )
    user_task: Optional["UserTask"] = Relationship(back_populates="documents")
