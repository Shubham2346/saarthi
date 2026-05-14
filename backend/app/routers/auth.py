import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database import get_session
from app.schemas.user import (
    GoogleAuthRequest,
    EmailLoginRequest,
    EmailRegisterRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    RefreshRequest,
    UserRead,
)
from app.services.auth_service import (
    verify_google_token,
    get_or_create_user,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    verify_password,
    get_user_by_email,
    get_user_by_id,
)
from app.services.rbac_service import (
    assign_role_to_user, get_user_permissions, seed_default_roles,
    seed_permissions, seed_role_permissions,
)
from app.services.task_service import assign_all_tasks_to_user
from app.middleware.auth import get_current_user
from app.models.user import User, UserRole
from app.config import get_settings
from app.services.email_service import send_email
from app.services.password_reset_service import (
    create_password_reset_token,
    consume_password_reset_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/google", response_model=TokenResponse)
async def google_login(
    request: GoogleAuthRequest,
    session: AsyncSession = Depends(get_session),
):
    google_info = await verify_google_token(request.token)
    user, is_new = await get_or_create_user(session, google_info)

    if is_new:
        await assign_all_tasks_to_user(session, user.id)

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)
    permissions = await get_user_permissions(session, user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
        permissions=permissions,
    )


@router.post("/register", response_model=TokenResponse)
async def email_register(
    request: EmailRegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user with email and password. Optional role selection."""
    existing_user = await get_user_by_email(session, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    role = request.role or UserRole.STUDENT
    user = User(
        email=request.email,
        full_name=request.name,
        hashed_password=hash_password(request.password),
        google_id=f"email_{request.email}",
        role=role,
        is_system_admin=(role == UserRole.SYSTEM_ADMIN),
    )
    session.add(user)
    await session.flush()

    # Seed RBAC infrastructure and assign role
    await seed_default_roles(session)
    await seed_permissions(session)
    await seed_role_permissions(session)
    await assign_role_to_user(session, user, role.value)

    # Assign onboarding tasks to new students
    await assign_all_tasks_to_user(session, user.id)
    await session.commit()

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)
    permissions = await get_user_permissions(session, user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
        permissions=permissions,
    )


@router.post("/login", response_model=TokenResponse)
async def email_login(
    request: EmailLoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """Authenticate with email and password."""
    user = await get_user_by_email(session, request.email)
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)
    permissions = await get_user_permissions(session, user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
        permissions=permissions,
    )


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    user = await get_user_by_email(session, request.email)

    if user and user.hashed_password:
        raw_token = await create_password_reset_token(session, user)
        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={raw_token}"
        subject = f"Reset your {settings.APP_NAME} password"
        html = (
            f"<p>Hi {user.full_name},</p>"
            f"<p>We received a request to reset your password. Click the link below (valid for "
            f"{settings.PASSWORD_RESET_TOKEN_HOURS} hours):</p>"
            f'<p><a href="{reset_url}">Reset password</a></p>'
            f"<p>If you did not request this, you can ignore this email.</p>"
        )
        await send_email(user.email, subject, html, reset_url)

    return {"message": "If an account exists for that email, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    session: AsyncSession = Depends(get_session),
):
    user = await consume_password_reset_token(session, request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset link. Please request a new one.",
        )

    user.hashed_password = hash_password(request.password)
    user.updated_at = datetime.utcnow()
    session.add(user)

    return {"message": "Your password has been updated. You can sign in now."}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request: RefreshRequest,
    session: AsyncSession = Depends(get_session),
):
    """Exchange a valid refresh token for a new access token."""
    from jose import JWTError

    try:
        payload = decode_access_token(request.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not a refresh token",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in refresh token",
        )

    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)
    permissions = await get_user_permissions(session, user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserRead.model_validate(user),
        permissions=permissions,
    )


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get the currently authenticated user's profile."""
    return UserRead.model_validate(current_user)


@router.get("/permissions")
async def get_my_permissions(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get the current user's permissions."""
    permissions = await get_user_permissions(session, current_user.id)
    return {"permissions": permissions, "role": current_user.role.value}
