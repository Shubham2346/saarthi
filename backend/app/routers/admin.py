"""
Admin router — dashboard, system stats, and user management.
All endpoints require admin privileges.
"""

import uuid
from typing import Optional
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from app.database import get_session
from app.schemas.user import UserRead, UserUpdate
from app.middleware.auth import require_admin
from app.models.user import User, UserRole, OnboardingStage, AdmissionStatus
from app.models.role import Role, UserRoleLink
from app.models.document import Document
from app.models.task import UserTask, TaskStatus
from app.models.ticket import SupportTicket, TicketStatus
from app.models.conversation import Conversation
from app.models.knowledge import KnowledgeEntry
from app.config import get_settings
from app.services.rbac_service import assign_role_to_user

router = APIRouter(prefix="/admin", tags=["Admin"])
settings = get_settings()


@router.get("/dashboard")
async def admin_dashboard(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get aggregated dashboard statistics for the admin panel."""
    # User counts by role
    total_users = (await session.execute(select(func.count(User.id)))).scalar() or 0
    student_count = (
        await session.execute(
            select(func.count(User.id)).where(User.role == UserRole.STUDENT)
        )
    ).scalar() or 0
    admin_count = (
        await session.execute(
            select(func.count(User.id)).where(User.role == UserRole.ADMIN)
        )
    ).scalar() or 0
    mentor_count = (
        await session.execute(
            select(func.count(User.id)).where(User.role == UserRole.MENTOR)
        )
    ).scalar() or 0

    # Admission funnel
    applied_count = (
        await session.execute(
            select(func.count(User.id)).where(
                User.admission_status.in_([
                    AdmissionStatus.APPLIED,
                    AdmissionStatus.DOCUMENTS_UPLOADED,
                    AdmissionStatus.DOCUMENTS_VERIFIED,
                ])
            )
        )
    ).scalar() or 0
    approved_count = (
        await session.execute(
            select(func.count(User.id)).where(User.admission_status == AdmissionStatus.APPROVED)
        )
    ).scalar() or 0
    enrolled_count = (
        await session.execute(
            select(func.count(User.id)).where(User.admission_status == AdmissionStatus.ENROLLED)
        )
    ).scalar() or 0

    # Document counts
    total_docs = (await session.execute(select(func.count(Document.id)))).scalar() or 0
    pending_docs = (
        await session.execute(
            select(func.count(Document.id)).where(
                Document.status == "uploaded"
            )
        )
    ).scalar() or 0

    # Task completion stats
    total_tasks = (await session.execute(select(func.count(UserTask.id)))).scalar() or 0
    completed_tasks = (
        await session.execute(
            select(func.count(UserTask.id)).where(
                UserTask.status == TaskStatus.COMPLETED
            )
        )
    ).scalar() or 0

    # Ticket stats
    open_tickets = (
        await session.execute(
            select(func.count(SupportTicket.id)).where(
                SupportTicket.status == TicketStatus.OPEN
            )
        )
    ).scalar() or 0

    # Conversation stats
    total_convs = (
        await session.execute(select(func.count(Conversation.id))).scalar() or 0
    )

    # Knowledge base
    total_kb = (
        await session.execute(select(func.count(KnowledgeEntry.id))).scalar() or 0
    )

    return {
        "users": {
            "total": total_users,
            "students": student_count,
            "admins": admin_count,
            "mentors": mentor_count,
        },
        "admissions": {
            "applied": applied_count,
            "approved": approved_count,
            "enrolled": enrolled_count,
        },
        "documents": {
            "total": total_docs,
            "pending_verification": pending_docs,
        },
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "completion_rate": round(completed_tasks / total_tasks * 100, 1)
            if total_tasks > 0
            else 0,
        },
        "tickets": {
            "open": open_tickets,
        },
        "conversations": {
            "total": total_convs,
        },
        "knowledge_base": {
            "total_entries": total_kb,
        },
    }


@router.get("/users", response_model=list[UserRead])
async def admin_list_users(
    role: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """List all users with pagination and optional role filter."""
    statement = select(User)
    if role:
        statement = statement.where(User.role == role)
    statement = statement.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await session.execute(statement)
    return [UserRead.model_validate(u) for u in result.scalars().all()]


@router.get("/users/{user_id}", response_model=UserRead)
async def admin_get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get any user by ID (admin only)."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.patch("/users/{user_id}", response_model=UserRead)
async def admin_update_user(
    user_id: uuid.UUID,
    update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Update any user's profile including role changes, mentor assignment (admin only)."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


@router.post("/users/{user_id}/assign-mentor")
async def admin_assign_mentor(
    user_id: uuid.UUID,
    mentor_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Assign a faculty mentor to a student."""
    student = await session.get(User, user_id)
    if not student or student.role != UserRole.STUDENT:
        raise HTTPException(status_code=404, detail="Student not found")

    mentor = await session.get(User, mentor_id)
    if not mentor or mentor.role != UserRole.MENTOR:
        raise HTTPException(status_code=400, detail="Invalid mentor")

    student.mentor_id = mentor_id
    student.updated_at = datetime.utcnow()
    session.add(student)
    await session.commit()
    return {"message": "Mentor assigned successfully", "student_id": str(user_id), "mentor_id": str(mentor_id)}


@router.get("/mentors", response_model=list[UserRead])
async def admin_list_mentors(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """List all users with mentor role."""
    stmt = select(User).where(User.role == UserRole.MENTOR).order_by(User.full_name)
    result = await session.execute(stmt)
    return [UserRead.model_validate(u) for u in result.scalars().all()]


@router.delete("/users/{user_id}", status_code=204)
async def admin_delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Delete a user account (admin only). Irreversible."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == UserRole.SYSTEM_ADMIN:
        raise HTTPException(status_code=403, detail="Cannot delete system admin accounts")
    await session.delete(user)
    await session.commit()
    return None


@router.get("/system")
async def admin_system_info(
    _admin: User = Depends(require_admin),
):
    """Get system configuration and health information."""
    from app.database import engine
    from sqlalchemy import text

    db_status = "unknown"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "app": {
            "name": settings.APP_NAME,
            "version": settings.VERSION,
            "environment": settings.APP_ENV,
        },
        "database": {
            "url": str(settings.DATABASE_URL).split("@")[-1],
            "status": db_status,
        },
        "features": {
            "admin_dashboard": settings.ENABLE_ADMIN_DASHBOARD,
            "document_verification": settings.ENABLE_DOCUMENT_VERIFICATION,
            "rag_search": settings.ENABLE_RAG_SEARCH,
            "escalation_agent": settings.ENABLE_ESCALATION_AGENT,
        },
    }
