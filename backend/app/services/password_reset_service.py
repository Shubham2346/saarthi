"""Create and verify password-reset tokens."""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config import get_settings
from app.models.password_reset import PasswordResetToken
from app.models.user import User


def hash_reset_token(raw_token: str) -> str:
    settings = get_settings()
    return hashlib.sha256(f"{settings.JWT_SECRET}:{raw_token}".encode()).hexdigest()


async def invalidate_existing_tokens(session: AsyncSession, user_id: uuid.UUID) -> None:
    result = await session.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used_at.is_(None),
        )
    )
    for row in result.scalars().all():
        row.used_at = datetime.now(timezone.utc)
        session.add(row)


async def create_password_reset_token(session: AsyncSession, user: User) -> str:
    """
    Invalidate prior open tokens, create a new one, return the raw token
    (only returned once — caller must email it).
    """
    await invalidate_existing_tokens(session, user.id)

    settings = get_settings()
    raw = secrets.token_urlsafe(32)
    token_hash = hash_reset_token(raw)
    expires = datetime.now(timezone.utc) + timedelta(hours=settings.PASSWORD_RESET_TOKEN_HOURS)

    row = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires,
    )
    session.add(row)
    await session.flush()
    return raw


async def consume_password_reset_token(
    session: AsyncSession, raw_token: str
) -> Optional[User]:
    """If token is valid and unused, mark used and return the user."""
    token_hash = hash_reset_token(raw_token)
    result = await session.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    )
    row = result.scalar_one_or_none()
    if not row or row.used_at is not None:
        return None

    now = datetime.now(timezone.utc)
    exp = row.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if now > exp:
        return None

    row.used_at = now
    session.add(row)

    ures = await session.execute(select(User).where(User.id == row.user_id))
    user = ures.scalar_one_or_none()
    return user
