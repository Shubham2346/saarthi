"""
Agentic co-filling of the structured admission application.
Uses heuristic/regex extraction only — no LLM/Ollama dependency.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.admission_application import AdmissionApplication
from app.models.user import User

APPLICATION_STRING_FIELDS: Tuple[str, ...] = (
    "full_name",
    "email",
    "phone",
    "address_line1",
    "city",
    "state",
    "postal_code",
    "country",
    "program_choice",
    "previous_institution",
    "board_10",
    "percentage_10",
    "board_12",
    "percentage_12",
    "guardian_name",
    "guardian_phone",
    "extracurriculars",
    "statement_of_purpose",
)


def _heuristic_fields(message: str) -> Dict[str, str]:
    """Extract structured fields from natural language using regex."""
    out: Dict[str, str] = {}

    # Name extraction
    m = re.search(
        r"(?:my name is|i am|i'm|this is|call me)\s+([A-Za-z][A-Za-z\s'.-]{1,80})",
        message,
        re.I,
    )
    if m:
        out["full_name"] = m.group(1).strip().title()

    # Email extraction
    m = re.search(
        r"(?:email|mail|e-mail)\s*(?:is|:)?\s*([\w.+-]+@[\w.-]+\.\w+)",
        message,
        re.I,
    )
    if m:
        out["email"] = m.group(1).lower()

    # Phone extraction
    m = re.search(
        r"(?:phone|mobile|whatsapp|call me at|contact)\s*(?:is|:)?\s*(\+?\d[\d\s\-]{8,18}\d)",
        message,
        re.I,
    )
    if m:
        out["phone"] = re.sub(r"[\s\-]", "", m.group(1))

    # Program/course/branch preference
    m = re.search(
        r"(?:program|course|branch|want to study|interested in|prefer)\s*(?:is|:)?\s*([A-Za-z][A-Za-z0-9\s,&\-]{2,120})",
        message,
        re.I,
    )
    if m:
        out["program_choice"] = m.group(1).strip()

    # City
    m = re.search(
        r"(?:city|live in|from)\s*(?:is|:)?\s*([A-Za-z][A-Za-z\s\-]{1,60})",
        message,
        re.I,
        # Avoid matching words like "from" as city names
    )
    if m and m.group(1).strip().lower() not in ("home",):
        out["city"] = m.group(1).strip().title()

    # State
    m = re.search(
        r"(?:state)\s*(?:is|:)?\s*([A-Za-z][A-Za-z\s\-]{1,60})",
        message,
        re.I,
    )
    if m:
        out["state"] = m.group(1).strip().title()

    # CET/JEE score
    m = re.search(
        r"(?:cet|jee|percentile|score)\s*(?:is|:)?\s*(\d{2}(?:\.\d+)?)",
        message,
        re.I,
    )
    if m:
        out.setdefault("extracurriculars", "")
        score_info = f"CET/JEE Score: {m.group(1)}"
        if out["extracurriculars"]:
            out["extracurriculars"] += f"; {score_info}"
        else:
            out["extracurriculars"] = score_info

    # 10th/12th percentage
    m = re.search(
        r"(?:10th|10|ssc|matric)\s*(?:percentage|marks|score|%)\s*(?:is|:)?\s*(\d{2}(?:\.\d+)?)",
        message,
        re.I,
    )
    if m:
        out["percentage_10"] = m.group(1)

    m = re.search(
        r"(?:12th|12|hsc|intermediate)\s*(?:percentage|marks|score|%)\s*(?:is|:)?\s*(\d{2}(?:\.\d+)?)",
        message,
        re.I,
    )
    if m:
        out["percentage_12"] = m.group(1)

    return out


def _parse_dob(val: str) -> Optional[date]:
    try:
        parts = val.strip()[:10].split("-")
        if len(parts) == 3:
            y, mo, d = int(parts[0]), int(parts[1]), int(parts[2])
            return date(y, mo, d)
    except (ValueError, IndexError):
        return None
    return None


def _compute_pipeline_percent(app: AdmissionApplication) -> int:
    filled = 0
    total = len(APPLICATION_STRING_FIELDS) + 1
    for key in APPLICATION_STRING_FIELDS:
        v = getattr(app, key, None)
        if v is not None and str(v).strip():
            filled += 1
    if app.date_of_birth is not None:
        filled += 1
    if total == 0:
        return 0
    return int(round(100 * filled / total))


def application_to_dict(app: AdmissionApplication) -> Dict[str, Any]:
    return {
        "id": str(app.id),
        "full_name": app.full_name,
        "email": app.email,
        "phone": app.phone,
        "date_of_birth": app.date_of_birth.isoformat() if app.date_of_birth else None,
        "address_line1": app.address_line1,
        "city": app.city,
        "state": app.state,
        "postal_code": app.postal_code,
        "country": app.country,
        "program_choice": app.program_choice,
        "previous_institution": app.previous_institution,
        "board_10": app.board_10,
        "percentage_10": app.percentage_10,
        "board_12": app.board_12,
        "percentage_12": app.percentage_12,
        "guardian_name": app.guardian_name,
        "guardian_phone": app.guardian_phone,
        "extracurriculars": app.extracurriculars,
        "statement_of_purpose": app.statement_of_purpose,
        "pipeline_percent": app.pipeline_percent,
        "updated_at": app.updated_at.isoformat() if app.updated_at else None,
    }


async def get_or_create_application(
    session: AsyncSession, user: User
) -> AdmissionApplication:
    result = await session.execute(
        select(AdmissionApplication).where(AdmissionApplication.user_id == user.id)
    )
    app = result.scalar_one_or_none()
    if app:
        return app
    app = AdmissionApplication(
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        pipeline_percent=0,
    )
    app.pipeline_percent = _compute_pipeline_percent(app)
    session.add(app)
    await session.flush()
    return app


def _apply_field_updates(
    app: AdmissionApplication, updates: Dict[str, Any]
) -> List[str]:
    changed: List[str] = []
    for key, val in updates.items():
        if val is None:
            continue
        if key == "date_of_birth":
            if isinstance(val, str):
                parsed = _parse_dob(val)
                if parsed and app.date_of_birth != parsed:
                    app.date_of_birth = parsed
                    changed.append(key)
            continue
        if key in APPLICATION_STRING_FIELDS and isinstance(val, str):
            nv = val.strip()
            if not nv:
                continue
            cur = getattr(app, key, None)
            if cur != nv:
                lim = 4000 if key == "statement_of_purpose" else 2000
                setattr(app, key, nv[:lim])
                changed.append(key)
    app.updated_at = datetime.utcnow()
    app.pipeline_percent = _compute_pipeline_percent(app)
    return changed


async def merge_manual_updates(
    session: AsyncSession, user: User, updates: Dict[str, Any]
) -> AdmissionApplication:
    """Apply explicit field edits from the UI."""
    app = await get_or_create_application(session, user)
    _apply_field_updates(app, {k: v for k, v in updates.items() if v is not None})
    session.add(app)
    await session.flush()
    return app


def _generate_assistant_reply(
    changed: List[str],
    application: AdmissionApplication,
    user_message: str,
) -> str:
    """Generate a contextual reply based on what fields were updated and what's missing."""
    msg_lower = user_message.lower()

    if not changed:
        missing = []
        for key in APPLICATION_STRING_FIELDS:
            v = getattr(application, key, None)
            if not v or not str(v).strip():
                missing.append(key)

        if any(w in msg_lower for w in ["hello", "hi", "hey", "start", "begin"]):
            return (
                "Welcome to the AI Admission Assistant! I can help you fill out your "
                "admission application step by step.\n\n"
                "To get started, tell me about yourself. For example:\n"
                "- Your full name, email, and phone number\n"
                "- Your preferred program/branch (e.g., Computer Engineering)\n"
                "- Your 10th and 12th percentage marks\n"
                "- Your city and state\n\n"
                "Or you can fill in the form fields directly on the right panel."
            )

        if missing:
            hints = []
            if "full_name" in missing:
                hints.append("your full name")
            if "program_choice" in missing:
                hints.append("which branch you want to study")
            if "percentage_10" in missing or "percentage_12" in missing:
                hints.append("your 10th/12th percentage marks")
            if "city" in missing or "state" in missing:
                hints.append("your city and state")
            if "guardian_name" in missing:
                hints.append("your parent/guardian name")

            if hints:
                hint_text = ", ".join(hints[:3])
                if len(hints) > 3:
                    hint_text += f", and {len(hints) - 3} more details"
                return (
                    f"You can tell me more details like {hint_text}. "
                    "Every bit of information helps complete your application!"
                )

        return (
            "I'm here to help fill your admission application. "
            "You can tell me your details in natural language, and I'll update the form. "
            "For example: 'My name is Rahul, I scored 85% in 12th, and I want Computer Engineering.'"
        )

    return (
        f"Great! I've updated the following field(s) in your application: "
        f"{', '.join(changed)}. "
        f"Your application is now {application.pipeline_percent}% complete. "
        "Keep going — tell me more about yourself!"
    )


async def process_admission_turn(
    session: AsyncSession,
    user: User,
    user_message: str,
) -> Dict[str, Any]:
    """
    Run one agentic turn: merge heuristics into DB, return payload for API/UI.
    No LLM/Ollama used — pure regex extraction and template responses.
    """
    app = await get_or_create_application(session, user)
    heuristic = _heuristic_fields(user_message)
    changed = _apply_field_updates(app, heuristic)
    session.add(app)

    assistant_reply = _generate_assistant_reply(changed, app, user_message)

    return {
        "message": assistant_reply,
        "application": application_to_dict(app),
        "fields_updated": changed,
        "pipeline_percent": app.pipeline_percent,
    }
