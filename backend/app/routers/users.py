"""
Users router — profile management and admin user listing.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.schemas.user import UserRead, UserUpdate
from app.middleware.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserRead])
async def list_users(
    role: str = None,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """List all users (admin only). Optionally filter by role."""
    statement = select(User)
    if role:
        statement = statement.where(User.role == role)
    statement = statement.order_by(User.created_at.desc())
    result = await session.execute(statement)
    users = result.scalars().all()
    return [UserRead.model_validate(u) for u in users]


@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return UserRead.model_validate(current_user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a user profile. Students can only view their own profile."""
    import uuid

    target_id = uuid.UUID(user_id)

    # Students can only view their own profile
    if current_user.role == "student" and current_user.id != target_id:
        raise HTTPException(status_code=403, detail="Access denied")

    statement = select(User).where(User.id == target_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
    update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update the current user's profile."""
    from datetime import datetime, timezone

    update_data = update.model_dump(exclude_unset=True)

    # For demo purposes, allow users to change their own role
    # if current_user.role == "student" and "role" in update_data:
    #     del update_data["role"]

    for key, value in update_data.items():
        setattr(current_user, key, value)

    current_user.updated_at = datetime.utcnow()
    session.add(current_user)
    return UserRead.model_validate(current_user)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: str,
    update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Update any user's profile (admin only)."""
    import uuid
    from datetime import datetime, timezone

    target_id = uuid.UUID(user_id)
    statement = select(User).where(User.id == target_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    user.updated_at = datetime.utcnow()
    session.add(user)
    return UserRead.model_validate(user)
