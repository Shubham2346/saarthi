"""
Knowledge Base model — tracks ingested FAQ/document entries
that are stored in the Vector Database for RAG retrieval.
"""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class KnowledgeCategory(str, enum.Enum):
    ADMISSION = "admission"
    FEE = "fee"
    HOSTEL = "hostel"
    ACADEMIC = "academic"
    LMS = "lms"
    EXAM = "exam"
    PLACEMENT = "placement"
    GENERAL = "general"


class KnowledgeEntry(SQLModel, table=True):
    """
    Tracks each piece of knowledge ingested into the vector DB.
    This acts as the 'source of truth' registry — the actual embeddings
    live in ChromaDB, but this table lets admins manage, update, and
    delete entries through the dashboard.
    """

    __tablename__ = "knowledge_entries"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Content
    question: str = Field(max_length=500)
    answer: str = Field()
    category: KnowledgeCategory = Field()

    # Source tracking
    source: str = Field(default="manual", max_length=100)  # manual, pdf, web, etc.
    source_file: Optional[str] = Field(default=None, max_length=255)

    # Vector DB reference
    chroma_id: Optional[str] = Field(default=None, max_length=255, index=True)

    # Metadata
    is_active: bool = Field(default=True)
    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
