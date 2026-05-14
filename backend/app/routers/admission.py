"""Admission application API + agentic assistant (also reachable via /chat intent)."""

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.admission import (
    AdmissionApplicationRead,
    AdmissionApplicationPatch,
    AdmissionAssistantChatRequest,
    AdmissionAssistantChatResponse,
)
from app.services.admission_assistant_service import (
    application_to_dict,
    get_or_create_application,
    merge_manual_updates,
    process_admission_turn,
)

router = APIRouter(prefix="/admission", tags=["Admission AI"])


def _as_read(d: Dict[str, Any]) -> AdmissionApplicationRead:
    return AdmissionApplicationRead.model_validate(d)


@router.get("/application", response_model=AdmissionApplicationRead)
async def get_my_application(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Return the current user's admission draft (auto-seeded from profile when new)."""
    app = await get_or_create_application(session, current_user)
    return _as_read(application_to_dict(app))


@router.patch("/application", response_model=AdmissionApplicationRead)
async def patch_my_application(
    body: AdmissionApplicationPatch,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Manually edit application fields from the live form."""
    data = body.model_dump(exclude_unset=True)
    if "email" in data and data["email"] is not None:
        data["email"] = str(data["email"])
    app = await merge_manual_updates(session, current_user, data)
    return _as_read(application_to_dict(app))


@router.post("/assistant/chat", response_model=AdmissionAssistantChatResponse)
async def admission_assistant_chat(
    body: AdmissionAssistantChatRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    One conversational turn for the admission copilot (same engine as LangGraph admission node,
    callable directly for the split-pane UI without streaming).
    """
    out = await process_admission_turn(session, current_user, body.message)
    return AdmissionAssistantChatResponse(
        answer=out["message"],
        application=out["application"],
        pipeline_percent=out["pipeline_percent"],
        fields_updated=out["fields_updated"],
    )
