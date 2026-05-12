"""
Documents router — file upload, listing, and admin verification.
"""

import os
import uuid
import shutil
from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.config import get_settings
from app.schemas.document import DocumentRead, DocumentVerify
from app.middleware.auth import get_current_user, require_admin
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.services.document_service import process_uploaded_document
from app.database import async_session

settings = get_settings()
router = APIRouter(prefix="/documents", tags=["Documents"])

# Allowed file types for document uploads
ALLOWED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/tiff",
}


@router.post("/upload", response_model=DocumentRead, status_code=201)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    task_id: str = Form(default=None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a document for verification.

    - Validates file type and size.
    - Stores the file on disk.
    - Creates a database record with 'uploaded' status.
    - Triggers the Document Verification Agent in the background.
    """
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed. "
            f"Allowed: {', '.join(ALLOWED_TYPES)}",
        )

    # Read file and check size
    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # Create upload directory structure: uploads/<user_id>/
    user_dir = os.path.join(settings.UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)

    # Generate unique filename
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(user_dir, unique_filename)

    # Write file to disk
    with open(file_path, "wb") as f:
        f.write(content)

    # Create database record
    parsed_task_id = uuid.UUID(task_id) if task_id else None
    document = Document(
        user_id=current_user.id,
        task_id=parsed_task_id,
        filename=unique_filename,
        original_filename=file.filename or "unknown",
        file_path=file_path,
        file_type=file.content_type or "application/octet-stream",
        file_size_bytes=len(content),
        status=DocumentStatus.UPLOADED,
    )
    session.add(document)
    await session.flush()
    
    # Trigger background verification
    async def run_verification(doc_id: uuid.UUID):
        async with async_session() as bg_session:
            await process_uploaded_document(bg_session, doc_id)
            
    background_tasks.add_task(run_verification, document.id)

    return DocumentRead.model_validate(document)


@router.get("/my-documents", response_model=List[DocumentRead])
async def list_my_documents(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List all documents uploaded by the current user."""
    statement = (
        select(Document)
        .where(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
    )
    result = await session.execute(statement)
    docs = result.scalars().all()
    return [DocumentRead.model_validate(d) for d in docs]


@router.get("/pending", response_model=List[DocumentRead])
async def list_pending_documents(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """List all documents awaiting admin verification (admin only)."""
    statement = (
        select(Document)
        .where(Document.status == DocumentStatus.UPLOADED)
        .order_by(Document.created_at.asc())
    )
    result = await session.execute(statement)
    docs = result.scalars().all()
    return [DocumentRead.model_validate(d) for d in docs]


@router.patch("/{doc_id}/verify", response_model=DocumentRead)
async def verify_document(
    doc_id: uuid.UUID,
    verification: DocumentVerify,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
):
    """
    Verify or reject a document (admin only).
    Sets the verification status and records the admin who verified.
    """
    statement = select(Document).where(Document.id == doc_id)
    result = await session.execute(statement)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if verification.status not in (DocumentStatus.VERIFIED, DocumentStatus.REJECTED):
        raise HTTPException(
            status_code=400,
            detail="Status must be 'verified' or 'rejected'",
        )

    document.status = verification.status
    document.verified_by = admin.id
    document.verified_at = datetime.utcnow()

    if verification.status == DocumentStatus.REJECTED:
        document.rejection_reason = verification.rejection_reason

    session.add(document)
    await session.flush()

    return DocumentRead.model_validate(document)


@router.get("/{doc_id}", response_model=DocumentRead)
async def get_document(
    doc_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a specific document's details."""
    statement = select(Document).where(Document.id == doc_id)
    result = await session.execute(statement)
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Students can only view their own documents
    if current_user.role == "student" and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return DocumentRead.model_validate(document)
