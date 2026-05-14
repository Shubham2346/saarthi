"""
Task models — OnboardingTask (templates) and UserTask (per-student assignments).
Supports categorized, ordered checklists with deadlines and status tracking.
"""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document


class TaskCategory(str, enum.Enum):
    DOCUMENT = "document"
    FEE = "fee"
    ACADEMIC = "academic"
    ORIENTATION = "orientation"
    GENERAL = "general"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class OnboardingTask(SQLModel, table=True):
    """Template task — defines what students need to complete during onboarding."""

    __tablename__ = "onboarding_tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    category: TaskCategory = Field()
    sort_order: int = Field(default=0)
    is_mandatory: bool = Field(default=True)
    deadline: Optional[datetime] = Field(default=None)
    requires_document: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user_tasks: List["UserTask"] = Relationship(back_populates="task")


class UserTask(SQLModel, table=True):
    """Per-student task assignment with status and progress tracking."""

    __tablename__ = "user_tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    task_id: uuid.UUID = Field(foreign_key="onboarding_tasks.id", index=True)

    status: TaskStatus = Field(default=TaskStatus.PENDING)
    notes: Optional[str] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="user_tasks",
        sa_relationship_kwargs={"foreign_keys": "[UserTask.user_id]"},
    )
    task: Optional["OnboardingTask"] = Relationship(back_populates="user_tasks")
    documents: List["Document"] = Relationship(back_populates="user_task")
