import uuid
from typing import Optional, Callable, List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.services.auth_service import decode_access_token, get_user_by_id
from app.models.user import User, UserRole
from app.models.role import Permission, RolePermission, UserRoleLink, Role
from app.services.rbac_service import get_user_permissions

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )

    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


# --- Role-based guards ---

async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in (UserRole.ADMIN, UserRole.SYSTEM_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


async def require_admin_or_mentor(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in (UserRole.ADMIN, UserRole.MENTOR, UserRole.SYSTEM_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Mentor access required",
        )
    return current_user


async def require_system_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_system_admin and current_user.role != UserRole.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System admin access required",
        )
    return current_user


async def require_mentor(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Mentor access required",
        )
    return current_user


async def require_coordinator(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.DEPARTMENT_COORDINATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department coordinator access required",
        )
    return current_user


async def require_role(*roles: UserRole) -> Callable:
    async def _role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to: {', '.join(r.value for r in roles)}",
            )
        return current_user
    return _role_checker


# --- Permission-based guard ---

async def require_permission(permission_code: str) -> Callable:
    async def _permission_checker(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ) -> User:
        # System admin bypasses all permission checks
        if current_user.is_system_admin or current_user.role == UserRole.SYSTEM_ADMIN:
            return current_user

        # Admin has broad access
        if current_user.role == UserRole.ADMIN:
            return current_user

        # Coordinators bypass for department-related permissions
        if current_user.role == UserRole.DEPARTMENT_COORDINATOR and "admission" in permission_code:
            return current_user

        user_perms = await get_user_permissions(session, current_user.id)
        if permission_code not in user_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission_code}",
            )
        return current_user
    return _permission_checker
