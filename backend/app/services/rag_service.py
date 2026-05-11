"""
RAG (Retrieval-Augmented Generation) service — the core of the FAQ Agent.

Orchestrates the full RAG pipeline:
1. Takes a student's question.
2. Retrieves relevant FAQ entries from ChromaDB.
3. Constructs a context-enriched prompt.
4. Sends it to Ollama for a grounded response.
"""

import uuid
from typing import List, Optional, Dict, Any, AsyncGenerator

from app.services.ollama_service import ollama_service
from app.services.vector_store import vector_store

# System prompt for the RAG-powered FAQ agent
FAQ_SYSTEM_PROMPT = """You are **Saarthi**, a helpful and friendly AI assistant for college students going through the onboarding and admission process.

Your role:
- Answer student questions about admissions, fees, hostel, academics, LMS, exams, placements, and general college info.
- Be warm, encouraging, and concise. Students may be nervous — make them feel welcome.
- Always base your answers on the provided CONTEXT from the college knowledge base.
- If the context contains the answer, provide it clearly with relevant details.
- If the context does NOT contain enough information to answer, say: "I don't have specific information about that yet. I'd recommend contacting the relevant department or raising a support ticket through the portal."
- Never make up information. Never hallucinate details like dates, amounts, or contact info that aren't in the context.
- Format your response in a clean, readable way. Use numbered lists or bullet points when listing steps or items.
- Keep responses concise but thorough — aim for 2-4 paragraphs max.

Remember: You are Saarthi, the student's guide. Be helpful, be accurate, be kind."""


class RAGService:
    """Retrieval-Augmented Generation pipeline for the FAQ agent."""

    def __init__(self):
        self.ollama = ollama_service
        self.vector_store = vector_store

    async def query(
        self,
        question: str,
        category: Optional[str] = None,
        n_context: int = 5,
        temperature: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Full RAG pipeline: retrieve → augment → generate.

        Returns a dict with the answer, source documents, and metadata.
        """
        # Step 1: Retrieve relevant documents from ChromaDB
        try:
            results = self.vector_store.query(
                query_text=question,
                n_results=n_context,
                category_filter=category,
            )
        except Exception as e:
            return {
                "answer": "I'm having trouble accessing the knowledge base right now. Please try again in a moment or contact the helpdesk.",
                "sources": [],
                "error": str(e),
            }

        # Step 2: Build context from retrieved documents
        context_parts = []
        sources = []

        if results and results.get("documents"):
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                context_parts.append(
                    f"[Source {i + 1}] (Category: {metadata.get('category', 'N/A')})\n"
                    f"Q: {metadata.get('question', 'N/A')}\n"
                    f"A: {doc}"
                )
                sources.append({
                    "question": metadata.get("question", ""),
                    "category": metadata.get("category", ""),
                    "relevance_score": round(1 - distance, 3) if distance else 0,
                })

        context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant information found in the knowledge base."

        # Step 3: Construct the augmented prompt
        augmented_prompt = f"""CONTEXT FROM KNOWLEDGE BASE:
{context}

---

STUDENT'S QUESTION:
{question}

Please answer the student's question based on the context above. If the context doesn't contain relevant information, acknowledge that and suggest they contact the appropriate department."""

        # Step 4: Generate response using Ollama
        try:
            answer = await self.ollama.generate(
                prompt=augmented_prompt,
                system_prompt=FAQ_SYSTEM_PROMPT,
                temperature=temperature,
            )
        except Exception as e:
            return {
                "answer": "I'm currently unable to generate a response. The AI service might be temporarily unavailable. Please try again later or contact the helpdesk for immediate assistance.",
                "sources": sources,
                "error": str(e),
            }

        return {
            "answer": answer,
            "sources": sources,
            "context_used": len(sources),
        }

    async def query_stream(
        self,
        question: str,
        category: Optional[str] = None,
        n_context: int = 5,
        temperature: float = 0.5,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming RAG pipeline — yields response tokens for real-time display.
        Used for the SSE (Server-Sent Events) chat endpoint.
        """
        # Retrieve context
        try:
            results = self.vector_store.query(
                query_text=question,
                n_results=n_context,
                category_filter=category,
            )
        except Exception:
            yield "I'm having trouble accessing the knowledge base. Please try again."
            return

        # Build context
        context_parts = []
        if results and results.get("documents"):
            for i, (doc, metadata) in enumerate(
                zip(results["documents"][0], results["metadatas"][0])
            ):
                context_parts.append(
                    f"[Source {i + 1}] (Category: {metadata.get('category', 'N/A')})\n"
                    f"Q: {metadata.get('question', 'N/A')}\n"
                    f"A: {doc}"
                )

        context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant information found."

        augmented_prompt = f"""CONTEXT FROM KNOWLEDGE BASE:
{context}

---

STUDENT'S QUESTION:
{question}

Please answer the student's question based on the context above."""

        # Stream response
        try:
            async for chunk in self.ollama.generate_stream(
                prompt=augmented_prompt,
                system_prompt=FAQ_SYSTEM_PROMPT,
                temperature=temperature,
            ):
                yield chunk
        except Exception:
            yield "\n\n[Error: Unable to generate response. Please try again.]"

    async def search_knowledge_base(
        self,
        query: str,
        category: Optional[str] = None,
        n_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base without generating an LLM response.
        Useful for admin tools and debugging.
        """
        results = self.vector_store.query(
            query_text=query,
            n_results=n_results,
            category_filter=category,
        )

        entries = []
        if results and results.get("documents"):
            for doc, metadata, distance, doc_id in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
                results["ids"][0],
            ):
                entries.append({
                    "id": doc_id,
                    "question": metadata.get("question", ""),
                    "answer": doc,
                    "category": metadata.get("category", ""),
                    "relevance_score": round(1 - distance, 3) if distance else 0,
                })

        return entries


# Singleton instance
rag_service = RAGService()
