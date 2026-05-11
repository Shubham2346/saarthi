"""
Knowledge base entry request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.knowledge import KnowledgeCategory


class KnowledgeEntryCreate(BaseModel):
    """Create a new knowledge base entry."""
    question: str
    answer: str
    category: KnowledgeCategory
    source: str = "manual"


class KnowledgeEntryRead(BaseModel):
    """Knowledge entry returned in API responses."""
    id: uuid.UUID
    question: str
    answer: str
    category: KnowledgeCategory
    source: str
    source_file: Optional[str] = None
    chroma_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeEntryUpdate(BaseModel):
    """Update a knowledge base entry."""
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[KnowledgeCategory] = None
