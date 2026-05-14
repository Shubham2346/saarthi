import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.middleware.auth import require_admin, require_system_admin, get_current_user
from app.models.user import User, UserRole
from app.models.role import Role, Permission, RolePermission, UserRoleLink
from app.schemas.user import RoleRead, PermissionRead
from app.services.rbac_service import (
    seed_default_roles, seed_permissions, seed_role_permissions,
    assign_role_to_user, get_user_permissions, get_user_roles,
)

router = APIRouter(prefix="/roles", tags=["Roles & Permissions"])


@router.get("/", response_model=list[RoleRead])
async def list_roles(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    stmt = select(Role).order_by(Role.name)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/permissions", response_model=list[PermissionRead])
async def list_permissions(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    stmt = select(Permission).order_by(Permission.resource, Permission.action)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/my")
async def get_my_roles_and_permissions(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    roles = await get_user_roles(session, current_user.id)
    permissions = await get_user_permissions(session, current_user.id)
    return {
        "user_id": str(current_user.id),
        "primary_role": current_user.role.value,
        "roles": roles,
        "permissions": permissions,
    }


@router.post("/seed")
async def seed_rbac(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Seed default roles, permissions, and role-permission mappings."""
    await seed_default_roles(session)
    await seed_permissions(session)
    await seed_role_permissions(session)
    await session.commit()
    return {"message": "RBAC roles and permissions seeded successfully"}


@router.post("/users/{user_id}/assign")
async def assign_role_to_user_endpoint(
    user_id: uuid.UUID,
    role_name: str,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_enum = UserRole(role_name) if role_name in ("student", "admin", "mentor") else None
    if role_enum:
        user.role = role_enum
    user.is_system_admin = (role_name == "system_admin")

    await assign_role_to_user(session, user, role_name)
    session.add(user)
    await session.commit()
    return {"message": f"Role '{role_name}' assigned to user", "user_id": str(user_id)}


@router.get("/users/{user_id}")
async def get_user_roles_endpoint(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    roles = await get_user_roles(session, user_id)
    permissions = await get_user_permissions(session, user_id)
    return {
        "user_id": str(user_id),
        "roles": roles,
        "permissions": permissions,
    }
