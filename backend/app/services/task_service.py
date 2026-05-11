"""
Task service — business logic for managing onboarding tasks and student assignments.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.task import OnboardingTask, UserTask, TaskStatus
from app.models.user import User


async def create_onboarding_task(
    session: AsyncSession, task_data: dict
) -> OnboardingTask:
    """Create a new onboarding task template."""
    task = OnboardingTask(**task_data)
    session.add(task)
    await session.flush()
    return task


async def get_all_onboarding_tasks(
    session: AsyncSession,
) -> List[OnboardingTask]:
    """Fetch all onboarding task templates, ordered by sort_order."""
    statement = select(OnboardingTask).order_by(OnboardingTask.sort_order)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_onboarding_task_by_id(
    session: AsyncSession, task_id: uuid.UUID
) -> Optional[OnboardingTask]:
    """Fetch a single onboarding task template."""
    statement = select(OnboardingTask).where(OnboardingTask.id == task_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def update_onboarding_task(
    session: AsyncSession, task_id: uuid.UUID, update_data: dict
) -> OnboardingTask:
    """Update an onboarding task template."""
    task = await get_onboarding_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task template not found")
    for key, value in update_data.items():
        if value is not None:
            setattr(task, key, value)
    session.add(task)
    await session.flush()
    return task


async def delete_onboarding_task(
    session: AsyncSession, task_id: uuid.UUID
) -> bool:
    """Delete an onboarding task template."""
    task = await get_onboarding_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task template not found")
    await session.delete(task)
    return True


async def assign_all_tasks_to_user(
    session: AsyncSession, user_id: uuid.UUID
) -> List[UserTask]:
    """
    Assign all mandatory onboarding tasks to a new student.
    Called after user creation during auth flow.
    """
    tasks = await get_all_onboarding_tasks(session)
    user_tasks = []
    for task in tasks:
        if task.is_mandatory:
            user_task = UserTask(
                user_id=user_id,
                task_id=task.id,
                status=TaskStatus.PENDING,
            )
            session.add(user_task)
            user_tasks.append(user_task)
    await session.flush()
    return user_tasks


async def get_user_tasks(
    session: AsyncSession, user_id: uuid.UUID
) -> List[UserTask]:
    """Fetch all tasks assigned to a specific student, with task details."""
    statement = (
        select(UserTask)
        .where(UserTask.user_id == user_id)
        .options(selectinload(UserTask.task))
        .order_by(UserTask.created_at)
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def update_user_task(
    session: AsyncSession,
    user_task_id: uuid.UUID,
    user_id: uuid.UUID,
    update_data: dict,
) -> UserTask:
    """Update a student's task status."""
    statement = select(UserTask).where(
        UserTask.id == user_task_id,
        UserTask.user_id == user_id,
    )
    result = await session.execute(statement)
    user_task = result.scalar_one_or_none()

    if not user_task:
        raise HTTPException(status_code=404, detail="User task not found")

    for key, value in update_data.items():
        if value is not None:
            setattr(user_task, key, value)

    # Auto-set completed_at when status changes to completed
    if update_data.get("status") == TaskStatus.COMPLETED:
        user_task.completed_at = datetime.utcnow()

    user_task.updated_at = datetime.utcnow()
    session.add(user_task)
    await session.flush()
    return user_task


async def get_onboarding_progress(
    session: AsyncSession, user_id: uuid.UUID
) -> dict:
    """
    Calculate a student's overall onboarding progress.
    Returns completion stats for the dashboard.
    """
    user_tasks = await get_user_tasks(session, user_id)
    total = len(user_tasks)
    if total == 0:
        return {"total": 0, "completed": 0, "pending": 0, "percentage": 0}

    completed = sum(1 for t in user_tasks if t.status == TaskStatus.COMPLETED)
    pending = sum(1 for t in user_tasks if t.status == TaskStatus.PENDING)
    overdue = sum(1 for t in user_tasks if t.status == TaskStatus.OVERDUE)

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "in_progress": total - completed - pending - overdue,
        "percentage": round((completed / total) * 100, 1),
    }
