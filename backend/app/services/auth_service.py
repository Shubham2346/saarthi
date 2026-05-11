"""
Authentication service — handles Google OAuth verification, JWT creation,
and user lookup/creation.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.config import get_settings
from app.models.user import User, UserRole

settings = get_settings()


def create_access_token(user_id: uuid.UUID, role: str) -> str:
    """Create a signed JWT access token."""
    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token. Raises on failure."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_google_token(token: str) -> dict:
    """
    Verify a Google OAuth ID token and extract user info.
    Returns dict with: email, name, picture, sub (Google user ID).
    """
    if token == "dev-token" and settings.APP_ENV == "development":
        return {
            "sub": "dev-google-id-12345",
            "email": "student@example.com",
            "name": "Dev Student",
            "picture": "",
            "iss": "accounts.google.com"
        }

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Invalid issuer")
        return id_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {e}",
        )


async def get_or_create_user(
    session: AsyncSession, google_info: dict
) -> User:
    """
    Find an existing user by Google ID, or create a new one.
    Returns the User ORM instance.
    """
    google_id = google_info["sub"]

    # Try to find existing user
    statement = select(User).where(User.google_id == google_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user:
        # Update avatar if changed
        if google_info.get("picture") and user.avatar_url != google_info["picture"]:
            user.avatar_url = google_info["picture"]
            user.updated_at = datetime.utcnow()
            session.add(user)
        return user

    # Create new user
    user = User(
        email=google_info["email"],
        full_name=google_info.get("name", google_info["email"]),
        avatar_url=google_info.get("picture"),
        google_id=google_id,
        role=UserRole.STUDENT,
    )
    session.add(user)
    await session.flush()
    return user


async def get_user_by_id(
    session: AsyncSession, user_id: uuid.UUID
) -> Optional[User]:
    """Fetch a user by their primary key."""
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
