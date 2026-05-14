"""
Conversation model — tracks chat sessions between students and the multi-agent system.
Stores conversation history and metadata for turn tracking and analytics.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Text


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

    # Session tracking
    session_id: str = Field(max_length=255, index=True)
    turn_count: int = Field(default=0)

    # Conversation metadata
    title: Optional[str] = Field(default=None, max_length=500)
    intent_summary: Optional[str] = Field(default=None, max_length=1000)
    agent_sequence: Optional[str] = Field(default=None, sa_column=Column(Text))

    # Escalation tracking
    was_escalated: bool = Field(default=False)
    escalation_reason: Optional[str] = Field(default=None, max_length=1000)
    escalation_ticket_id: Optional[str] = Field(default=None, max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
