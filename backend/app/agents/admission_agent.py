"""LangGraph node — agentic admission form co-pilot."""

import uuid

from sqlmodel import select

from app.agents.state import AgentState
from app.database import async_session
from app.models.user import User
from app.services.admission_assistant_service import process_admission_turn


async def admission_node(state: AgentState) -> dict:
    uid = state.get("user_id") or ""
    if not uid:
        return {
            "response": "Please sign in to use the AI admission assistant.",
            "messages": [{
                "role": "assistant",
                "content": "Admission agent: missing user id",
                "agent": "admission",
                "metadata": None,
            }],
        }

    try:
        user_uuid = uuid.UUID(uid)
    except ValueError:
        return {
            "response": "We couldn't verify your session. Please refresh and try again.",
            "messages": [],
        }

    async with async_session() as session:
        try:
            result = await session.execute(select(User).where(User.id == user_uuid))
            user = result.scalar_one_or_none()
            if not user:
                return {
                    "response": "Account not found. Please sign in again.",
                    "messages": [],
                }

            out = await process_admission_turn(
                session, user, state.get("user_message", "")
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            return {
                "response": (
                    "Something went wrong while updating your application. "
                    "Please try again in a moment."
                ),
                "error": str(e)[:200],
                "messages": [{
                    "role": "system",
                    "content": f"Admission agent error: {str(e)[:120]}",
                    "agent": "admission",
                    "metadata": None,
                }],
            }

    return {
        "response": out["message"],
        "context": {
            "admission_application": out["application"],
            "admission_pipeline_percent": out["pipeline_percent"],
            "admission_fields_updated": out["fields_updated"],
        },
        "messages": [{
            "role": "assistant",
            "content": (
                f"Admission agent updated fields: {out['fields_updated'] or 'none'}; "
                f"pipeline {out['pipeline_percent']}%"
            ),
            "agent": "admission",
            "metadata": {"fields_updated": out["fields_updated"]},
        }],
    }
