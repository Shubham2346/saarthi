"""
Authentication router — Google OAuth login and token refresh.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.user import GoogleAuthRequest, TokenResponse, UserRead
from app.services.auth_service import (
    verify_google_token,
    get_or_create_user,
    create_access_token,
)
from app.services.task_service import assign_all_tasks_to_user
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/google", response_model=TokenResponse)
async def google_login(
    request: GoogleAuthRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate with Google OAuth.

    1. Frontend sends the Google ID token.
    2. Backend verifies it with Google.
    3. Creates or fetches the user.
    4. Assigns onboarding tasks if new user.
    5. Returns a JWT access token.
    """
    # Verify the Google token
    google_info = await verify_google_token(request.token)

    # Get or create user
    user, is_new = await get_or_create_user(session, google_info)

    # Assign onboarding tasks to new students
    if is_new:
        await assign_all_tasks_to_user(session, user.id)

    # Generate JWT
    access_token = create_access_token(user.id, user.role.value)

    return TokenResponse(
        access_token=access_token,
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get the currently authenticated user's profile."""
    return UserRead.model_validate(current_user)
