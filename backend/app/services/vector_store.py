"""
Vector Store service — manages ChromaDB for FAQ/Knowledge Base storage and retrieval.
Handles collection management, document ingestion, and similarity search.
"""

import uuid
from typing import List, Optional, Dict, Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import get_settings

settings = get_settings()


class VectorStoreService:
    """Manages ChromaDB collections for the RAG knowledge base."""

    COLLECTION_NAME = "saarthi_knowledge_base"

    def __init__(self):
        self._client: Optional[chromadb.ClientAPI] = None

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
        """Get or create the main knowledge base collection."""
        return self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Saarthi student onboarding knowledge base"},
        )

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str],
        embeddings: Optional[List[List[float]]] = None,
    ) -> None:
        """
        Add documents to the vector store.
        If embeddings are provided, they are used directly.
        Otherwise, ChromaDB will use its default embedding function.
        """
        kwargs = {
            "documents": documents,
            "metadatas": metadatas,
            "ids": ids,
        }
        if embeddings:
            kwargs["embeddings"] = embeddings

        self.collection.add(**kwargs)

    def query(
        self,
        query_text: Optional[str] = None,
        query_embedding: Optional[List[float]] = None,
        n_results: int = 5,
        category_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.

        Args:
            query_text: Text query (uses ChromaDB's default embeddings).
            query_embedding: Pre-computed embedding vector.
            n_results: Number of results to return.
            category_filter: Optional category to filter results.

        Returns:
            Dict with documents, metadatas, distances, and ids.
        """
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

        results = self.collection.query(**kwargs)
        return results

    def delete_by_id(self, doc_id: str) -> None:
        """Delete a document from the vector store by ID."""
        self.collection.delete(ids=[doc_id])

    def delete_by_ids(self, doc_ids: List[str]) -> None:
        """Delete multiple documents from the vector store."""
        if doc_ids:
            self.collection.delete(ids=doc_ids)

    def update_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict[str, Any],
        embedding: Optional[List[float]] = None,
    ) -> None:
        """Update an existing document in the vector store."""
        kwargs = {
            "ids": [doc_id],
            "documents": [document],
            "metadatas": [metadata],
        }
        if embedding:
            kwargs["embeddings"] = [embedding]

        self.collection.update(**kwargs)

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.COLLECTION_NAME,
                "document_count": count,
                "status": "healthy",
            }
        except Exception as e:
            return {
                "collection_name": self.COLLECTION_NAME,
                "status": "error",
                "message": str(e),
            }

    def reset_collection(self) -> None:
        """Delete and recreate the collection (use with caution!)."""
        try:
            self.client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass  # Collection might not exist
        # Re-accessing the property will recreate it
        _ = self.collection


# Singleton instance
vector_store = VectorStoreService()
