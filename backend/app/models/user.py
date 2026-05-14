import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.task import UserTask
    from app.models.document import Document
    from app.models.ticket import SupportTicket
    from app.models.password_reset import PasswordResetToken
    from app.models.admission_application import AdmissionApplication
    from app.models.role import UserRoleLink


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    MENTOR = "mentor"
    SYSTEM_ADMIN = "system_admin"
    DEPARTMENT_COORDINATOR = "department_coordinator"


class OnboardingStage(str, enum.Enum):
    PRE_ADMISSION = "pre_admission"
    DOCUMENTS = "documents"
    FEE_PAYMENT = "fee_payment"
    ORIENTATION = "orientation"
    COMPLETED = "completed"


class AdmissionStatus(str, enum.Enum):
    NOT_APPLIED = "not_applied"
    APPLIED = "applied"
    DOCUMENTS_UPLOADED = "documents_uploaded"
    DOCUMENTS_VERIFIED = "documents_verified"
    APPROVED = "approved"
    REJECTED = "rejected"
    ENROLLED = "enrolled"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=500)

    # Authentication
    google_id: str = Field(unique=True, index=True, max_length=255)
    hashed_password: Optional[str] = Field(default=None, max_length=255)

    # Role & Profile
    role: UserRole = Field(default=UserRole.STUDENT)
    phone: Optional[str] = Field(default=None, max_length=20)
    admission_id: Optional[str] = Field(default=None, max_length=50, index=True)

    # Admission flow
    admission_status: AdmissionStatus = Field(default=AdmissionStatus.NOT_APPLIED)

    # Mentor assignment (FK to another user)
    mentor_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)

    # System admin flag (very restricted)
    is_system_admin: bool = Field(default=False)

    # Onboarding Progress
    stage: OnboardingStage = Field(default=OnboardingStage.PRE_ADMISSION)

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
    password_reset_tokens: List["PasswordResetToken"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[PasswordResetToken.user_id]"},
    )
    admission_application: Optional["AdmissionApplication"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "[AdmissionApplication.user_id]",
            "uselist": False,
        },
    )

    # Assigned students (if user is a mentor)
    mentored_students: List["User"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "User.mentor_id",
            "remote_side": "User.id",
        },
    )

    # Role links (many-to-many with roles table)
    role_links: List["UserRoleLink"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"viewonly": True},
    )
