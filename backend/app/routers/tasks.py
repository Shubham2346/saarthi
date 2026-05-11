"""
Tasks router — onboarding task templates (admin) and student task assignments.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.task import (
    OnboardingTaskCreate, OnboardingTaskRead, OnboardingTaskUpdate,
    UserTaskRead, UserTaskUpdate, UserTaskWithDetails,
)
from app.services.task_service import (
    create_onboarding_task,
    get_all_onboarding_tasks,
    get_onboarding_task_by_id,
    update_onboarding_task,
    delete_onboarding_task,
    get_user_tasks,
    update_user_task,
    get_onboarding_progress,
    assign_all_tasks_to_user,
)
from app.middleware.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ======================
# ONBOARDING TASK TEMPLATES (admin)
# ======================

@router.post("/templates", response_model=OnboardingTaskRead, status_code=201)
async def create_task_template(
    task: OnboardingTaskCreate,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Create a new onboarding task template (admin only)."""
    new_task = await create_onboarding_task(session, task.model_dump())
    return OnboardingTaskRead.model_validate(new_task)


@router.get("/templates", response_model=List[OnboardingTaskRead])
async def list_task_templates(
    session: AsyncSession = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    """List all onboarding task templates."""
    tasks = await get_all_onboarding_tasks(session)
    return [OnboardingTaskRead.model_validate(t) for t in tasks]


@router.get("/templates/{task_id}", response_model=OnboardingTaskRead)
async def get_task_template(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    """Get a specific onboarding task template."""
    task = await get_onboarding_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task template not found")
    return OnboardingTaskRead.model_validate(task)


@router.patch("/templates/{task_id}", response_model=OnboardingTaskRead)
async def update_task_template(
    task_id: uuid.UUID,
    update: OnboardingTaskUpdate,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Update a task template (admin only)."""
    updated = await update_onboarding_task(
        session, task_id, update.model_dump(exclude_unset=True)
    )
    return OnboardingTaskRead.model_validate(updated)


@router.delete("/templates/{task_id}", status_code=204)
async def delete_task_template(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Delete a task template (admin only)."""
    await delete_onboarding_task(session, task_id)
    return None


# ======================
# USER TASKS (student assignments)
# ======================

@router.get("/my-tasks", response_model=List[UserTaskWithDetails])
async def get_my_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get the current student's onboarding task list with details."""
    user_tasks = await get_user_tasks(session, current_user.id)
    result = []
    for ut in user_tasks:
        task_read = OnboardingTaskRead.model_validate(ut.task) if ut.task else None
        result.append(
            UserTaskWithDetails(
                id=ut.id,
                status=ut.status,
                notes=ut.notes,
                completed_at=ut.completed_at,
                task=task_read,
            )
        )
    return result


@router.get("/my-progress")
async def get_my_progress(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get the current student's onboarding progress summary."""
    return await get_onboarding_progress(session, current_user.id)


@router.patch("/my-tasks/{user_task_id}", response_model=UserTaskRead)
async def update_my_task(
    user_task_id: uuid.UUID,
    update: UserTaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update a specific task's status (e.g., mark as in_progress or completed)."""
    updated = await update_user_task(
        session,
        user_task_id,
        current_user.id,
        update.model_dump(exclude_unset=True),
    )
    return UserTaskRead.model_validate(updated)


@router.get("/user/{user_id}/tasks", response_model=List[UserTaskRead])
async def get_user_tasks_admin(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get a specific student's tasks (admin only)."""
    tasks = await get_user_tasks(session, user_id)
    return [UserTaskRead.model_validate(t) for t in tasks]


@router.get("/user/{user_id}/progress")
async def get_user_progress_admin(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get a specific student's progress (admin only)."""
    return await get_onboarding_progress(session, user_id)


@router.post("/user/{user_id}/assign-all", status_code=201)
async def assign_tasks_to_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Assign all mandatory tasks to a specific student (admin only)."""
    user_tasks = await assign_all_tasks_to_user(session, user_id)
    return {"assigned": len(user_tasks)}
