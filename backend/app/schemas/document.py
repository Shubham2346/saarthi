"""
Document request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.document import DocumentStatus


class DocumentRead(BaseModel):
    """Document data returned in API responses."""
    id: uuid.UUID
    user_id: uuid.UUID
    task_id: Optional[uuid.UUID] = None
    filename: str
    original_filename: str
    file_type: str
    file_size_bytes: int
    document_type: Optional[str] = None
    status: DocumentStatus
    rejection_reason: Optional[str] = None
    ocr_text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    verified_by: Optional[uuid.UUID] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentVerify(BaseModel):
    """Admin action to verify or reject a document."""
    status: DocumentStatus  # verified or rejected
    rejection_reason: Optional[str] = None
