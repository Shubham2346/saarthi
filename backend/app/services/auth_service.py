"""
Authentication service — handles Google OAuth verification, JWT creation,
and user lookup/creation.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from jose import jwt, JWTError
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from passlib.context import CryptContext
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.config import get_settings
from app.models.user import User, UserRole
from app.services.rbac_service import assign_role_to_user, seed_default_roles, seed_permissions, seed_role_permissions

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: uuid.UUID, role: str) -> str:
    """Create a signed JWT access token (short-lived)."""
    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: uuid.UUID) -> str:
    """Create a signed JWT refresh token (long-lived)."""
    expire = datetime.utcnow() + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


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
    session: AsyncSession, google_info: dict,
    role_name: Optional[str] = None,
) -> Tuple[User, bool]:
    """
    Find an existing user by Google ID, or create a new one.

    Returns (user, created) where created is True only for a newly inserted row.
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
        return user, False

    # Determine role
    role = UserRole.STUDENT
    if role_name:
        try:
            role = UserRole(role_name)
        except ValueError:
            role = UserRole.STUDENT

    # Create new user
    user = User(
        email=google_info["email"],
        full_name=google_info.get("name", google_info["email"]),
        avatar_url=google_info.get("picture"),
        google_id=google_id,
        role=role,
        is_system_admin=(role == UserRole.SYSTEM_ADMIN),
    )
    session.add(user)
    await session.flush()

    # Seed roles and assign user role
    await seed_default_roles(session)
    await seed_permissions(session)
    await seed_role_permissions(session)
    await assign_role_to_user(session, user, role.value)

    return user, True


async def get_user_by_id(
    session: AsyncSession, user_id: uuid.UUID
) -> Optional[User]:
    """Fetch a user by their primary key."""
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_email(
    session: AsyncSession, email: str
) -> Optional[User]:
    """Fetch a user by email."""
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
