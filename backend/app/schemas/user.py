"""
User request/response schemas for API validation.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole, OnboardingStage


# --- Auth Schemas ---

class GoogleAuthRequest(BaseModel):
    """Request body when frontend sends a Google OAuth token."""
    token: str


class TokenResponse(BaseModel):
    """JWT access token returned after successful authentication."""
    access_token: str
    token_type: str = "bearer"
    user: "UserRead"


# --- User CRUD Schemas ---

class UserCreate(BaseModel):
    """Manual user creation (admin use)."""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT
    phone: Optional[str] = None
    admission_id: Optional[str] = None


class UserRead(BaseModel):
    """User data returned in API responses."""
    id: uuid.UUID
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    role: UserRole
    phone: Optional[str] = None
    admission_id: Optional[str] = None
    stage: OnboardingStage
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Fields that can be updated on a user profile."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    admission_id: Optional[str] = None
    stage: Optional[OnboardingStage] = None
    role: Optional[UserRole] = None  # admin only


# Fix forward reference
TokenResponse.model_rebuild()
