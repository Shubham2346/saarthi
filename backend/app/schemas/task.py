"""
Task request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.task import TaskCategory, TaskStatus


# --- OnboardingTask (template) ---

class OnboardingTaskCreate(BaseModel):
    """Create a new onboarding task template (admin)."""
    title: str
    description: Optional[str] = None
    category: TaskCategory
    sort_order: int = 0
    is_mandatory: bool = True
    deadline: Optional[datetime] = None
    requires_document: bool = False


class OnboardingTaskRead(BaseModel):
    """Onboarding task template data."""
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    category: TaskCategory
    sort_order: int
    is_mandatory: bool
    deadline: Optional[datetime] = None
    requires_document: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OnboardingTaskUpdate(BaseModel):
    """Updatable fields for a task template."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TaskCategory] = None
    sort_order: Optional[int] = None
    is_mandatory: Optional[bool] = None
    deadline: Optional[datetime] = None
    requires_document: Optional[bool] = None


# --- UserTask (student assignment) ---

class UserTaskRead(BaseModel):
    """Student's assigned task status."""
    id: uuid.UUID
    user_id: uuid.UUID
    task_id: uuid.UUID
    status: TaskStatus
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserTaskUpdate(BaseModel):
    """Update a student's task status."""
    status: Optional[TaskStatus] = None
    notes: Optional[str] = None


class UserTaskWithDetails(BaseModel):
    """UserTask enriched with the parent OnboardingTask info for the dashboard."""
    id: uuid.UUID
    status: TaskStatus
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    task: OnboardingTaskRead

    class Config:
        from_attributes = True
