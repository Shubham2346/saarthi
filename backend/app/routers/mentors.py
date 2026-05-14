from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models.user import User, UserRole
from app.schemas.user import UserRead
from app.middleware.auth import get_current_user, require_admin_or_mentor, require_admin

router = APIRouter(prefix="/mentors", tags=["Mentors"])

@router.get("/students", response_model=List[UserRead])
async def get_my_students(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin_or_mentor),
):
    """(Section 2.10) Get students assigned to the current mentor."""
    statement = select(User).where(User.mentor_id == current_user.id)
    result = await session.execute(statement)
    students = result.scalars().all()
    return [UserRead.model_validate(s) for s in students]

@router.patch("/{mentor_id}/assign/{student_id}", response_model=UserRead)
async def assign_student_to_mentor(
    mentor_id: str,
    student_id: str,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """(Section 2.10) Map a student to a mentor (Admin only)."""
    import uuid
    m_id = uuid.UUID(mentor_id)
    s_id = uuid.UUID(student_id)
    
    # Verify mentor exists and has correct role
    mentor = await session.get(User, m_id)
    if not mentor or mentor.role not in [UserRole.MENTOR, UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=404, detail="Valid mentor not found")
        
    student = await session.get(User, s_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    student.mentor_id = m_id
    session.add(student)
    
    # Audit logging could be inserted here
    
    return UserRead.model_validate(student)
