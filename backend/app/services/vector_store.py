"""
Vector Store service — manages ChromaDB for FAQ/Knowledge Base storage and retrieval.
Handles collection management, document ingestion, and similarity search.
All public methods are async to avoid blocking the event loop.
Uses Ollama embeddings via nomic-embed-text for semantic search.
"""

import uuid
import asyncio
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from app.config import get_settings

settings = get_settings()

# Thread pool for blocking ChromaDB calls
_chroma_executor = ThreadPoolExecutor(max_workers=4)


class VectorStoreService:
    """Manages ChromaDB collections for the RAG knowledge base."""

    COLLECTION_NAME = "saarthi_knowledge_base"

    def __init__(self):
        self._client: Optional[chromadb.ClientAPI] = None
        self._embedding_fn = DefaultEmbeddingFunction()

    @property
    def client(self) -> chromadb.ClientAPI:
        """Lazy-initialize the ChromaDB persistent client."""
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        """Get or create the main knowledge base collection with Ollama embeddings."""
        return self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self._embedding_fn,
            metadata={"description": "Saarthi student onboarding knowledge base"},
        )

    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str],
        embeddings: Optional[List[List[float]]] = None,
    ) -> None:
        kwargs = {
            "documents": documents,
            "metadatas": metadatas,
            "ids": ids,
        }
        if embeddings:
            kwargs["embeddings"] = embeddings

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _chroma_executor, lambda: self.collection.add(**kwargs)
        )

    async def query(
        self,
        query_text: Optional[str] = None,
        query_embedding: Optional[List[float]] = None,
        n_results: int = 5,
        category_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}

        kwargs = {
            "n_results": n_results,
        }

        if query_embedding:
            kwargs["query_embeddings"] = [query_embedding]
        elif query_text:
            kwargs["query_texts"] = [query_text]
        else:
            raise ValueError("Either query_text or query_embedding must be provided")

        if where_filter:
            kwargs["where"] = where_filter

        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            _chroma_executor, lambda: self.collection.query(**kwargs)
        )
        return results

    async def delete_by_id(self, doc_id: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _chroma_executor, lambda: self.collection.delete(ids=[doc_id])
        )

    async def delete_by_ids(self, doc_ids: List[str]) -> None:
        if doc_ids:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _chroma_executor, lambda: self.collection.delete(ids=doc_ids)
            )

    async def update_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict[str, Any],
        embedding: Optional[List[float]] = None,
    ) -> None:
        kwargs = {
            "ids": [doc_id],
            "documents": [document],
            "metadatas": [metadata],
        }
        if embedding:
            kwargs["embeddings"] = [embedding]

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _chroma_executor, lambda: self.collection.update(**kwargs)
        )

    def get_collection_stats(self) -> Dict[str, Any]:
        try:
            count = self.collection.count()
            return {
                "collection_name": self.COLLECTION_NAME,
                "document_count": count,
                "embedding_model": settings.EMBEDDING_MODEL_NAME,
                "status": "healthy",
            }
        except Exception as e:
            return {
                "collection_name": self.COLLECTION_NAME,
                "status": "error",
                "message": str(e),
            }

    async def reset_collection(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _chroma_executor,
                lambda: self.client.delete_collection(self.COLLECTION_NAME),
            )
        except Exception:
            pass
        _ = self.collection


# Singleton instance
vector_store = VectorStoreService()
