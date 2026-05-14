"""
System Admin router — platform management, security, and monitoring.
Extremely restricted — hidden from normal UI.
"""

import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlmodel import select, func

from app.database import get_session, engine
from app.schemas.user import UserRead, UserUpdate
from app.middleware.auth import require_system_admin, get_current_user
from app.models.user import User, UserRole
from app.models.role import Role, Permission, RolePermission, UserRoleLink
from app.services.rbac_service import (
    assign_role_to_user, seed_default_roles, seed_permissions,
    seed_role_permissions, get_user_permissions,
)
from app.config import get_settings

router = APIRouter(prefix="/sysadmin", tags=["System Admin"])
settings = get_settings()


@router.get("/dashboard")
async def sysadmin_dashboard(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_system_admin),
):
    """System-level statistics and health overview."""
    total_users = (await session.execute(select(func.count(User.id)))).scalar() or 0
    total_roles = (await session.execute(select(func.count(Role.id)))).scalar() or 0
    total_permissions = (await session.execute(select(func.count(Permission.id)))).scalar() or 0

    db_status = "unknown"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "users": {"total": total_users},
        "roles": {"total": total_roles},
        "permissions": {"total": total_permissions},
        "database": {"status": db_status},
        "app": {
            "name": settings.APP_NAME,
            "version": settings.VERSION,
            "environment": settings.APP_ENV,
        },
    }


@router.get("/users", response_model=list[UserRead])
async def list_all_users(
    role: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_system_admin),
):
    """List all users with full details (system admin only)."""
    stmt = select(User)
    if role:
        stmt = stmt.where(User.role == role)
    stmt = stmt.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return [UserRead.model_validate(u) for u in result.scalars().all()]


@router.post("/users/{user_id}/role")
async def set_user_role(
    user_id: uuid.UUID,
    role_name: str,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_system_admin),
):
    """Change any user's role (system admin only)."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        role_enum = UserRole(role_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {role_name}")

    user.role = role_enum
    user.is_system_admin = (role_enum == UserRole.SYSTEM_ADMIN)
    user.updated_at = datetime.utcnow()
    session.add(user)

    await assign_role_to_user(session, user, role_name)
    await session.commit()
    return {"message": f"User role updated to {role_name}", "user_id": str(user_id)}


@router.get("/roles", response_model=list)
async def list_roles(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_system_admin),
):
    """List all roles with user counts."""
    stmt = select(Role).order_by(Role.name)
    result = await session.execute(stmt)
    roles = result.scalars().all()

    output = []
    for role in roles:
        count = (
            await session.execute(
                select(func.count(UserRoleLink.user_id)).where(
                    UserRoleLink.role_id == role.id
                )
            )
        ).scalar() or 0
        output.append({
            "id": str(role.id),
            "name": role.name,
            "description": role.description,
            "is_system": role.is_system,
            "user_count": count,
        })
    return output


@router.post("/roles/seed")
async def seed_rbac(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_system_admin),
):
    """Re-seed all RBAC roles, permissions, and mappings."""
    await seed_default_roles(session)
    await seed_permissions(session)
    await seed_role_permissions(session)
    await session.commit()
    return {"message": "RBAC seeded successfully"}


@router.get("/audit")
async def get_audit_logs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    _admin: User = Depends(require_system_admin),
):
    """Get system audit logs (placeholder — extend with actual audit model)."""
    return {
        "logs": [],
        "total": 0,
        "message": "Audit logging will be available in the next update",
    }


@router.get("/config")
async def get_system_config(
    _admin: User = Depends(require_system_admin),
):
    """View system configuration (sanitized — no secrets)."""
    return {
        "app": {
            "name": settings.APP_NAME,
            "version": settings.VERSION,
            "environment": settings.APP_ENV,
            "debug": settings.DEBUG,
        },
        "features": {
            "admin_dashboard": settings.ENABLE_ADMIN_DASHBOARD,
            "document_verification": settings.ENABLE_DOCUMENT_VERIFICATION,
            "rag_search": settings.ENABLE_RAG_SEARCH,
            "escalation_agent": settings.ENABLE_ESCALATION_AGENT,
            "vector_db": settings.ENABLE_VECTOR_DB,
        },
        "limits": {
            "max_upload_mb": settings.MAX_UPLOAD_SIZE_MB,
            "jwt_expiry_minutes": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        },
    }
