"""
User request/response schemas for API validation.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, AliasChoices
from app.models.user import UserRole, OnboardingStage, AdmissionStatus


# --- Auth Schemas ---

class GoogleAuthRequest(BaseModel):
    """Request body when frontend sends a Google OAuth ID token."""

    token: str = Field(validation_alias=AliasChoices("token", "id_token"))


class EmailLoginRequest(BaseModel):
    """Email/password login request."""
    email: EmailStr
    password: str


class EmailRegisterRequest(BaseModel):
    """Email/password signup request."""
    email: EmailStr
    password: str
    name: str
    role: Optional[UserRole] = Field(default=UserRole.STUDENT, description="User role during registration")


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password with token."""
    token: str
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    """JWT access token returned after successful authentication."""
    access_token: str
    refresh_token: str = ""
    token_type: str = "bearer"
    user: "UserRead"
    permissions: list[str] = []


class RefreshRequest(BaseModel):
    """Request a new access token using a refresh token."""
    refresh_token: str


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
    admission_status: AdmissionStatus = AdmissionStatus.NOT_APPLIED
    mentor_id: Optional[uuid.UUID] = None
    is_system_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Fields that can be updated on a user profile."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    admission_id: Optional[str] = None
    stage: Optional[OnboardingStage] = None
    role: Optional[UserRole] = None
    admission_status: Optional[AdmissionStatus] = None
    mentor_id: Optional[uuid.UUID] = None


# --- Permission Schemas ---

class PermissionRead(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    description: Optional[str] = None
    resource: str
    action: str

    class Config:
        from_attributes = True


class RoleRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    is_system: bool = False

    class Config:
        from_attributes = True


# Fix forward reference
TokenResponse.model_rebuild()
