"""
Coordinator router — Department-specific admissions management.
All endpoints require department_coordinator privileges.
"""

import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from app.database import get_session
from app.schemas.user import UserRead
from app.middleware.auth import require_coordinator, get_current_user
from app.models.user import User, UserRole, AdmissionStatus

router = APIRouter(prefix="/coordinator", tags=["Coordinator"])


@router.get("/dashboard")
async def coordinator_dashboard(
    session: AsyncSession = Depends(get_session),
    _coordinator: User = Depends(require_coordinator),
):
    """Get department-level admission statistics."""
    total_applicants = (
        await session.execute(
            select(func.count(User.id)).where(User.role == UserRole.STUDENT)
        )
    ).scalar() or 0

    pending_review = (
        await session.execute(
            select(func.count(User.id)).where(
                User.admission_status == AdmissionStatus.DOCUMENTS_UPLOADED,
                User.role == UserRole.STUDENT,
            )
        )
    ).scalar() or 0

    approved = (
        await session.execute(
            select(func.count(User.id)).where(
                User.admission_status == AdmissionStatus.APPROVED,
                User.role == UserRole.STUDENT,
            )
        )
    ).scalar() or 0

    enrolled = (
        await session.execute(
            select(func.count(User.id)).where(
                User.admission_status == AdmissionStatus.ENROLLED,
                User.role == UserRole.STUDENT,
            )
        )
    ).scalar() or 0

    return {
        "total_applicants": total_applicants,
        "pending_review": pending_review,
        "approved": approved,
        "enrolled": enrolled,
    }


@router.get("/students", response_model=list[UserRead])
async def list_department_students(
    status: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
    _coordinator: User = Depends(require_coordinator),
):
    """List students filtered by admission status."""
    stmt = select(User).where(User.role == UserRole.STUDENT)
    if status:
        stmt = stmt.where(User.admission_status == status)
    stmt = stmt.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return [UserRead.model_validate(u) for u in result.scalars().all()]


@router.get("/students/{student_id}", response_model=UserRead)
async def get_student_detail(
    student_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _coordinator: User = Depends(require_coordinator),
):
    """Get detailed student profile."""
    student = await session.get(User, student_id)
    if not student or student.role != UserRole.STUDENT:
        raise HTTPException(status_code=404, detail="Student not found")
    return UserRead.model_validate(student)


@router.patch("/students/{student_id}/status")
async def update_student_status(
    student_id: uuid.UUID,
    status: AdmissionStatus,
    session: AsyncSession = Depends(get_session),
    _coordinator: User = Depends(require_coordinator),
):
    """Update a student's admission status."""
    student = await session.get(User, student_id)
    if not student or student.role != UserRole.STUDENT:
        raise HTTPException(status_code=404, detail="Student not found")
    student.admission_status = status
    student.updated_at = datetime.utcnow()
    session.add(student)
    await session.commit()
    return {"message": f"Student status updated to {status.value}", "student_id": str(student_id)}
