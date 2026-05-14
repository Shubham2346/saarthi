"""
Knowledge Base router — admin endpoints for managing FAQ entries.
Handles CRUD operations that sync between PostgreSQL and ChromaDB.
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.knowledge import (
    KnowledgeEntryCreate,
    KnowledgeEntryRead,
    KnowledgeEntryUpdate,
)
from app.services.knowledge_service import knowledge_service
from app.middleware.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.post("/ingest-defaults", status_code=201)
async def ingest_default_faqs(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """
    Ingest the default FAQ dataset into the knowledge base.
    This populates ChromaDB and PostgreSQL with the seed FAQs.
    Idempotent — skips entries that already exist.
    """
    count = await knowledge_service.ingest_default_faqs(session)
    stats = await knowledge_service.get_vector_store_stats()

    return {
        "message": f"Successfully ingested {count} new FAQ entries",
        "new_entries": count,
        "vector_store": stats,
    }


@router.post("/entries", response_model=KnowledgeEntryRead, status_code=201)
async def create_entry(
    entry: KnowledgeEntryCreate,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
):
    """Add a new FAQ entry to the knowledge base (admin only)."""
    new_entry = await knowledge_service.ingest_single_entry(
        session=session,
        question=entry.question,
        answer=entry.answer,
        category=entry.category.value,
        source=entry.source,
        created_by=admin.id,
    )
    return KnowledgeEntryRead.model_validate(new_entry)


@router.get("/entries", response_model=List[KnowledgeEntryRead])
async def list_entries(
    category: Optional[str] = Query(default=None),
    active_only: bool = Query(default=True),
    session: AsyncSession = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    """List all knowledge base entries. Optionally filter by category."""
    entries = await knowledge_service.get_all_entries(
        session, category=category, active_only=active_only
    )
    return [KnowledgeEntryRead.model_validate(e) for e in entries]


@router.get("/entries/{entry_id}", response_model=KnowledgeEntryRead)
async def get_entry(
    entry_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    """Get a specific knowledge base entry."""
    entry = await knowledge_service.get_entry_by_id(session, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return KnowledgeEntryRead.model_validate(entry)


@router.patch("/entries/{entry_id}", response_model=KnowledgeEntryRead)
async def update_entry(
    entry_id: uuid.UUID,
    update: KnowledgeEntryUpdate,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Update a knowledge base entry (admin only). Syncs changes to ChromaDB."""
    entry = await knowledge_service.update_entry(
        session=session,
        entry_id=entry_id,
        question=update.question,
        answer=update.answer,
        category=update.category.value if update.category else None,
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return KnowledgeEntryRead.model_validate(entry)


@router.delete("/entries/{entry_id}", status_code=204)
async def delete_entry(
    entry_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Delete a knowledge base entry (admin only). Removes from both PostgreSQL and ChromaDB."""
    deleted = await knowledge_service.delete_entry(session, entry_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return None


@router.patch("/entries/{entry_id}/toggle", response_model=KnowledgeEntryRead)
async def toggle_entry_active(
    entry_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Toggle a knowledge entry between active/inactive (admin only)."""
    entry = await knowledge_service.toggle_active(session, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return KnowledgeEntryRead.model_validate(entry)


@router.get("/stats")
async def get_knowledge_stats(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get knowledge base statistics (admin only)."""
    from app.models.knowledge import KnowledgeEntry, KnowledgeCategory
    from sqlmodel import select, func

    # Count by category
    entries = await knowledge_service.get_all_entries(session, active_only=False)
    category_counts = {}
    active_count = 0
    inactive_count = 0

    for entry in entries:
        cat = entry.category.value
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if entry.is_active:
            active_count += 1
        else:
            inactive_count += 1

    vector_stats = await knowledge_service.get_vector_store_stats()

    return {
        "total_entries": len(entries),
        "active": active_count,
        "inactive": inactive_count,
        "by_category": category_counts,
        "vector_store": vector_stats,
    }
