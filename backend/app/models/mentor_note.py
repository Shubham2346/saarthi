"""
MentorNote model — stores notes that mentors write about assigned students.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class MentorNote(SQLModel, table=True):
    __tablename__ = "mentor_notes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    mentor_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
