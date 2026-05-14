"""Schemas for the agentic admission application."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AdmissionApplicationRead(BaseModel):
    id: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    program_choice: Optional[str] = None
    previous_institution: Optional[str] = None
    board_10: Optional[str] = None
    percentage_10: Optional[str] = None
    board_12: Optional[str] = None
    percentage_12: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    extracurriculars: Optional[str] = None
    statement_of_purpose: Optional[str] = None
    pipeline_percent: int = 0
    updated_at: Optional[str] = None


class AdmissionApplicationPatch(BaseModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=32)
    date_of_birth: Optional[str] = None
    address_line1: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=120)
    state: Optional[str] = Field(default=None, max_length=120)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    country: Optional[str] = Field(default=None, max_length=120)
    program_choice: Optional[str] = Field(default=None, max_length=255)
    previous_institution: Optional[str] = Field(default=None, max_length=255)
    board_10: Optional[str] = Field(default=None, max_length=64)
    percentage_10: Optional[str] = Field(default=None, max_length=32)
    board_12: Optional[str] = Field(default=None, max_length=64)
    percentage_12: Optional[str] = Field(default=None, max_length=32)
    guardian_name: Optional[str] = Field(default=None, max_length=255)
    guardian_phone: Optional[str] = Field(default=None, max_length=32)
    extracurriculars: Optional[str] = Field(default=None, max_length=2000)
    statement_of_purpose: Optional[str] = Field(default=None, max_length=4000)


class AdmissionAssistantChatRequest(BaseModel):
    """Optional dedicated endpoint body (same as chat message)."""

    message: str = Field(..., min_length=1, max_length=8000)


class AdmissionAssistantChatResponse(BaseModel):
    answer: str
    application: Dict[str, Any]
    pipeline_percent: int
    fields_updated: List[str] = []
