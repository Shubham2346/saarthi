"""
Knowledge Base management service — handles ingestion, updates, and deletion
of FAQ entries into both PostgreSQL (metadata) and ChromaDB (vectors).
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeEntry, KnowledgeCategory
from app.services.vector_store import vector_store
from app.data.default_faqs import DEFAULT_FAQS
from app.data.admission_knowledge import ADMISSION_KNOWLEDGE_BASE


class KnowledgeService:
    """Manages the dual-store knowledge base (PostgreSQL + ChromaDB)."""

    def __init__(self):
        self.vector_store = vector_store

    async def ingest_single_entry(
        self,
        session: AsyncSession,
        question: str,
        answer: str,
        category: str,
        source: str = "manual",
        created_by: Optional[uuid.UUID] = None,
    ) -> KnowledgeEntry:
        """
        Ingest a single FAQ entry into both PostgreSQL and ChromaDB.
        """
        chroma_id = str(uuid.uuid4())

        # 1. Create the document text for embedding (question + answer combined)
        doc_text = f"Question: {question}\nAnswer: {answer}"

        # 2. Add to ChromaDB
        await self.vector_store.add_documents(
            documents=[answer],  # Store answer as the document
            metadatas=[{
                "question": question,
                "category": category,
                "source": source,
            }],
            ids=[chroma_id],
        )

        # 3. Create PostgreSQL record
        entry = KnowledgeEntry(
            question=question,
            answer=answer,
            category=KnowledgeCategory(category),
            source=source,
            chroma_id=chroma_id,
            created_by=created_by,
        )
        session.add(entry)
        await session.flush()

        return entry

    async def ingest_default_faqs(self, session: AsyncSession) -> int:
        """
        Ingest all default FAQs AND admission knowledge base into the vector store.
        Skips entries that already exist (based on question text).
        Returns the number of new entries ingested.
        """
        count = 0
        all_entries = DEFAULT_FAQS + ADMISSION_KNOWLEDGE_BASE

        for faq in all_entries:
            # Check if already exists
            existing = await session.execute(
                select(KnowledgeEntry).where(
                    KnowledgeEntry.question == faq["question"]
                )
            )
            if existing.scalar_one_or_none():
                continue

            await self.ingest_single_entry(
                session=session,
                question=faq["question"],
                answer=faq["answer"],
                category=faq["category"],
                source="default_seed",
            )
            count += 1

        return count

    async def get_all_entries(
        self,
        session: AsyncSession,
        category: Optional[str] = None,
        active_only: bool = True,
    ) -> List[KnowledgeEntry]:
        """Get all knowledge base entries from PostgreSQL."""
        statement = select(KnowledgeEntry)

        if category:
            statement = statement.where(
                KnowledgeEntry.category == KnowledgeCategory(category)
            )
        if active_only:
            statement = statement.where(KnowledgeEntry.is_active == True)

        statement = statement.order_by(KnowledgeEntry.category, KnowledgeEntry.created_at)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_entry_by_id(
        self, session: AsyncSession, entry_id: uuid.UUID
    ) -> Optional[KnowledgeEntry]:
        """Get a single knowledge entry by ID."""
        statement = select(KnowledgeEntry).where(KnowledgeEntry.id == entry_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def update_entry(
        self,
        session: AsyncSession,
        entry_id: uuid.UUID,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Optional[KnowledgeEntry]:
        """
        Update a knowledge entry in both PostgreSQL and ChromaDB.
        """
        entry = await self.get_entry_by_id(session, entry_id)
        if not entry:
            return None

        # Update fields
        if question is not None:
            entry.question = question
        if answer is not None:
            entry.answer = answer
        if category is not None:
            entry.category = KnowledgeCategory(category)

        entry.updated_at = datetime.utcnow()
        session.add(entry)

        # Update in ChromaDB
        if entry.chroma_id:
            await self.vector_store.update_document(
                doc_id=entry.chroma_id,
                document=entry.answer,
                metadata={
                    "question": entry.question,
                    "category": entry.category.value,
                    "source": entry.source,
                },
            )

        await session.flush()
        return entry

    async def delete_entry(
        self, session: AsyncSession, entry_id: uuid.UUID
    ) -> bool:
        """Delete a knowledge entry from both PostgreSQL and ChromaDB."""
        entry = await self.get_entry_by_id(session, entry_id)
        if not entry:
            return False

        # Remove from ChromaDB
        if entry.chroma_id:
            try:
                await self.vector_store.delete_by_id(entry.chroma_id)
            except Exception:
                pass  # ChromaDB entry might already be gone

        # Remove from PostgreSQL
        await session.delete(entry)
        return True

    async def toggle_active(
        self, session: AsyncSession, entry_id: uuid.UUID
    ) -> Optional[KnowledgeEntry]:
        """Toggle the active/inactive status of a knowledge entry."""
        entry = await self.get_entry_by_id(session, entry_id)
        if not entry:
            return None

        entry.is_active = not entry.is_active
        entry.updated_at = datetime.utcnow()
        session.add(entry)
        await session.flush()
        return entry

    async def get_vector_store_stats(self) -> Dict[str, Any]:
        """Get ChromaDB collection statistics."""
        return self.vector_store.get_collection_stats()


# Singleton instance
knowledge_service = KnowledgeService()
