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
    from app.models.fee import FeeRecord
    from app.models.hostel import HostelAllocation


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    MENTOR = "mentor"
    SYSTEM_ADMIN = "system_admin"


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
    department: Optional[str] = Field(default=None, max_length=100)
    program: Optional[str] = Field(default=None, max_length=100)
    batch: Optional[str] = Field(default=None, max_length=20)

    # Mentor Mapping
    mentor_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)

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
    
    # Self-referential mentor relationship
    mentor: Optional["User"] = Relationship(
        back_populates="assigned_students",
        sa_relationship_kwargs={"remote_side": "[User.id]"}
    )
    assigned_students: List["User"] = Relationship(
        back_populates="mentor",
        sa_relationship_kwargs={"foreign_keys": "[User.mentor_id]"}
    )
    
    # Future relationships defined later
    fee_records: List["FeeRecord"] = Relationship(back_populates="user")
    hostel_allocation: Optional["HostelAllocation"] = Relationship(back_populates="user")
