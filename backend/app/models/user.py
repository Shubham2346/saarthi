"""
User model — supports students, admins, and mentors.
Tracks Google OAuth identity and onboarding stage.
"""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.task import UserTask
    from app.models.document import Document
    from app.models.ticket import SupportTicket


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    MENTOR = "mentor"


class OnboardingStage(str, enum.Enum):
    PRE_ADMISSION = "pre_admission"
    DOCUMENTS = "documents"
    FEE_PAYMENT = "fee_payment"
    ORIENTATION = "orientation"
    COMPLETED = "completed"


class User(SQLModel, table=True):
    """Core user entity supporting multi-role authentication."""

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=500)

    # Authentication
    google_id: str = Field(unique=True, index=True, max_length=255)
    hashed_password: Optional[str] = Field(default=None, max_length=255)

    # Role & Profile
    role: UserRole = Field(
        default=UserRole.STUDENT,
        sa_column=Column(SAEnum(UserRole), nullable=False, default=UserRole.STUDENT),
    )
    phone: Optional[str] = Field(default=None, max_length=20)
    admission_id: Optional[str] = Field(default=None, max_length=50, index=True)

    # Onboarding Progress
    stage: OnboardingStage = Field(
        default=OnboardingStage.PRE_ADMISSION,
        sa_column=Column(
            SAEnum(OnboardingStage),
            nullable=False,
            default=OnboardingStage.PRE_ADMISSION,
        ),
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # -- Relationships --
    user_tasks: List["UserTask"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[UserTask.user_id]"},
    )
    documents: List["Document"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Document.user_id]"},
    )
    tickets_created: List["SupportTicket"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[SupportTicket.user_id]"},
    )
