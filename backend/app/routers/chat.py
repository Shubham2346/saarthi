"""
Chat router — the student-facing multi-agent chat endpoint.

Phase 3 upgrade: Routes through the LangGraph multi-agent system instead of
direct RAG. The Supervisor classifies intent and routes to the right agent
(FAQ, Task, Escalation, or Greeting).

Still supports:
- Regular (non-streaming) responses via the agent graph
- Streaming SSE responses via direct RAG (fallback)
- Knowledge base search
- Health checks
"""

import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.chat import (
    ChatRequest, ChatResponse, ChatSource,
    KnowledgeSearchRequest, KnowledgeSearchResult,
)
from app.services.rag_service import rag_service
from app.services.ollama_service import ollama_service
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat / Multi-Agent"])


@router.post("/", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Chat with the Saarthi Multi-Agent System.

    The message flows through:
    1. **Supervisor** — classifies intent (faq, task, escalation, greeting)
    2. **Specialized Agent** — handles the request based on intent
    3. **Response** — returned with sources and metadata

    Set `stream: true` to receive a streaming SSE response (uses direct RAG).
    """
    if request.stream:
        # Streaming mode: use direct RAG pipeline (faster for streaming)
        return StreamingResponse(
            _stream_response(request.message, request.category),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # --- Multi-Agent Mode (default) ---
    from app.agents.graph import run_agent

    result = await run_agent(
        user_message=request.message,
        user_id=str(current_user.id),
        turn_count=0,  # TODO: track per-session turn count
    )

    # Build sources from agent result
    sources = []
    for s in result.get("sources", []):
        if isinstance(s, dict):
            sources.append(ChatSource(
                question=s.get("question", ""),
                category=s.get("category", ""),
                relevance_score=s.get("relevance_score", 0.0),
            ))

    return ChatResponse(
        answer=result.get("response", "I couldn't process your request."),
        sources=sources,
        context_used=len(sources),
        intent=result.get("intent", "unknown"),
        confidence=result.get("confidence", 0.0),
        agent_messages=[
            {
                "agent": m.get("agent", ""),
                "content": m.get("content", ""),
            }
            for m in result.get("messages", [])
            if m.get("role") in ("system", "assistant")
        ],
        error=result.get("error") if result.get("error") else None,
    )


@router.post("/direct", response_model=ChatResponse)
async def chat_direct_rag(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Bypass the multi-agent system and chat directly with the RAG pipeline.
    Useful for testing or when you only need FAQ-style answers.
    """
    result = await rag_service.query(
        question=request.message,
        category=request.category,
        temperature=0.5,
    )

    sources = [
        ChatSource(**s)
        for s in result.get("sources", [])
    ]

    return ChatResponse(
        answer=result.get("answer", ""),
        sources=sources,
        context_used=result.get("context_used", 0),
        intent="faq",
        confidence=1.0,
        error=result.get("error"),
    )


async def _stream_response(message: str, category: Optional[str] = None):
    """Generator for SSE streaming response using direct RAG."""
    try:
        async for chunk in rag_service.query_stream(
            question=message,
            category=category,
        ):
            data = json.dumps({"content": chunk})
            yield f"data: {data}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        error_data = json.dumps({"error": str(e)})
        yield f"data: {error_data}\n\n"


@router.post("/search", response_model=list[KnowledgeSearchResult])
async def search_knowledge_base(
    request: KnowledgeSearchRequest,
    _user: User = Depends(get_current_user),
):
    """
    Search the knowledge base directly without generating an LLM response.
    Useful for finding specific FAQ entries.
    """
    results = await rag_service.search_knowledge_base(
        query=request.query,
        category=request.category,
        n_results=request.n_results,
    )

    return [KnowledgeSearchResult(**r) for r in results]


@router.get("/health")
async def chat_health():
    """
    Check the health of the entire chat/agent system:
    - Ollama connectivity and model availability
    - Vector store (ChromaDB) status
    - Agent graph compilation status
    """
    ollama_status = await ollama_service.check_health()

    from app.services.vector_store import vector_store
    vector_status = vector_store.get_collection_stats()

    # Check agent graph
    try:
        from app.agents.graph import get_agent_graph
        graph = get_agent_graph()
        agent_status = {
            "status": "compiled",
            "nodes": list(graph.nodes.keys()) if hasattr(graph, 'nodes') else "unknown",
        }
    except Exception as e:
        agent_status = {"status": "error", "message": str(e)}

    return {
        "ollama": ollama_status,
        "vector_store": vector_status,
        "agent_graph": agent_status,
    }
