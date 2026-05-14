"""
Mentor router — assigned student management, notes, and communication.
All endpoints require mentor privileges.
"""

import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.middleware.auth import require_mentor, get_current_user
from app.models.user import User, UserRole
from app.schemas.user import UserRead

router = APIRouter(prefix="/mentor", tags=["Mentor"])


@router.get("/dashboard")
async def mentor_dashboard(
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """Get mentor dashboard overview with stats and recent activity."""
    from app.models.task import UserTask, TaskStatus

    students_stmt = select(User).where(
        User.mentor_id == current_user.id,
        User.role == UserRole.STUDENT,
    ).order_by(User.full_name)
    result = await session.execute(students_stmt)
    students = result.scalars().all()

    enrolled = sum(1 for s in students if s.admission_status.value == "enrolled")
    pending = sum(1 for s in students if s.admission_status.value not in ("enrolled", "rejected"))
    alerted = sum(1 for s in students if getattr(s, 'stage', '') == 'pre_admission' and s.admission_status.value == 'not_applied')

    return {
        "total_students": len(students),
        "enrolled": enrolled,
        "pending": pending,
        "needs_attention": alerted,
    }


@router.get("/students", response_model=list[UserRead])
async def list_assigned_students(
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """List all students assigned to this mentor."""
    stmt = select(User).where(
        User.mentor_id == current_user.id,
        User.role == UserRole.STUDENT,
    ).order_by(User.full_name)
    result = await session.execute(stmt)
    return [UserRead.model_validate(u) for u in result.scalars().all()]


@router.get("/students/{student_id}", response_model=UserRead)
async def get_student_detail(
    student_id: uuid.UUID,
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """Get detailed profile of an assigned student."""
    student = await session.get(User, student_id)
    if not student or student.mentor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Student not found or not assigned to you")
    return UserRead.model_validate(student)


@router.post("/students/{student_id}/notes")
async def add_mentor_note(
    student_id: uuid.UUID,
    note: str,
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """Add a mentor note for an assigned student."""
    student = await session.get(User, student_id)
    if not student or student.mentor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Student not found or not assigned to you")

    from app.models.mentor_note import MentorNote
    note_entry = MentorNote(
        mentor_id=current_user.id,
        student_id=student_id,
        content=note,
    )
    session.add(note_entry)
    await session.commit()
    return {"message": "Note added successfully"}


@router.get("/students/{student_id}/notes")
async def get_student_notes(
    student_id: uuid.UUID,
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """Get all mentor notes for an assigned student."""
    from app.models.mentor_note import MentorNote
    stmt = select(MentorNote).where(
        MentorNote.student_id == student_id,
        MentorNote.mentor_id == current_user.id,
    ).order_by(MentorNote.created_at.desc())
    result = await session.execute(stmt)
    notes = result.scalars().all()
    return [
        {
            "id": str(n.id),
            "content": n.content,
            "created_at": n.created_at.isoformat(),
        }
        for n in notes
    ]


@router.get("/stats")
async def mentor_stats(
    current_user: User = Depends(require_mentor),
    session: AsyncSession = Depends(get_session),
):
    """Get mentor summary statistics."""
    total_stmt = select(User).where(
        User.mentor_id == current_user.id,
        User.role == UserRole.STUDENT,
    )
    result = await session.execute(total_stmt)
    students = result.scalars().all()

    enrolled = sum(1 for s in students if s.admission_status.value == "enrolled")
    pending = sum(1 for s in students if s.admission_status.value not in ("enrolled", "rejected"))

    return {
        "total_students": len(students),
        "enrolled": enrolled,
        "pending": pending,
    }
