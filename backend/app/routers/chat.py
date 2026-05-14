"""
Chat router — the student-facing multi-agent chat endpoint.

Phase 3 upgrade: Routes through the LangGraph multi-agent system instead of
direct RAG. The Supervisor classifies intent and routes to the right agent
(FAQ, Task, Escalation, or Greeting).

Now supports:
- Multi-turn conversations with turn count tracking
- Conversation persistence via Conversation model
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
from app.services.conversation_service import conversation_service
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat / Multi-Agent"])


@router.post("/", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Chat with the Saarthi Multi-Agent System.

    The message flows through:
    1. **Supervisor** — classifies intent (faq, task, admission, escalation, greeting)
    2. **Specialized Agent** — handles the request based on intent
    3. **Response** — returned with sources, optional admission form snapshot, and metadata

    Set `stream: true` to receive a streaming SSE response (uses direct RAG).
    """
    if request.stream:
        return StreamingResponse(
            _stream_response(request.message, request.category),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # Get or create conversation for turn tracking
    conv = await conversation_service.get_or_create(
        session=session,
        user_id=current_user.id,
        conversation_id=request.conversation_id,
    )

    # --- Multi-Agent Mode (default) ---
    from app.agents.graph import run_agent

    result = await run_agent(
        user_message=request.message,
        user_id=str(current_user.id),
        conversation_id=str(conv.id),
        session_id=conv.session_id,
        student_name=current_user.full_name,
        student_email=current_user.email,
        turn_count=conv.turn_count,
    )

    # Increment turn count
    conv = await conversation_service.increment_turn(session, conv)

    # Update conversation metadata from agent result
    intent = result.get("intent", "unknown")
    agent_sequence = result.get("context", {}).get("agent_sequence", [])
    should_escalate = result.get("context", {}).get("should_escalate", False)
    escalation_reason = result.get("context", {}).get("escalation_reason")

    await conversation_service.update_metadata(
        session=session,
        conversation=conv,
        intent_summary=intent,
        agent_sequence=",".join(agent_sequence) if agent_sequence else None,
        was_escalated=bool(should_escalate),
        escalation_reason=escalation_reason,
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

    ctx = result.get("context") or {}
    admission_app = ctx.get("admission_application")
    admission_pct = ctx.get("admission_pipeline_percent")
    admission_changed = ctx.get("admission_fields_updated")

    # Build suggested next steps based on user's admission state
    suggested_steps = _get_suggested_next_steps(current_user)

    return ChatResponse(
        answer=result.get("response", "I couldn't process your request."),
        sources=sources,
        context_used=len(sources),
        intent=intent,
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
        admission_application=admission_app,
        admission_pipeline_percent=admission_pct,
        admission_fields_updated=admission_changed,
        conversation_id=str(conv.id),
        turn_count=conv.turn_count,
        user_role=current_user.role.value,
        user_admission_status=current_user.admission_status.value,
        user_onboarding_stage=current_user.stage.value,
        suggested_next_steps=suggested_steps,
    )


def _get_suggested_next_steps(user: User) -> list:
    """Generate contextual next steps based on user role and admission state."""
    if user.role.value in ("admin", "system_admin"):
        return [
            "Review pending applications in the Admin panel",
            "Verify uploaded student documents",
            "Assign mentors to approved students",
        ]

    if user.role.value == "mentor":
        return [
            "View your assigned students in the Mentor dashboard",
            "Check students needing attention",
            "Add mentoring notes for your students",
        ]

    if user.role.value == "department_coordinator":
        return [
            "Review department applications pending approval",
            "Check admission pipeline for your department",
            "Communicate with applicants needing documents",
        ]

    # Student-specific steps based on admission status
    stage_map = {
        "not_applied": [
            "Complete your admission application in the AI Admission section",
            "Upload required documents (marksheets, certificates, photo)",
            "Check eligibility requirements for your preferred branch",
        ],
        "applied": [
            "Upload remaining documents for verification",
            "Check your application status regularly",
            "Prepare for the next admission steps",
        ],
        "documents_uploaded": [
            "Wait for document verification by the admin team",
            "Check notification for verification updates",
            "Prepare original documents for physical verification",
        ],
        "documents_verified": [
            "Your documents are verified — awaiting admission decision",
            "Check application status in AI Admission section",
            "Prepare for admission confirmation steps",
        ],
        "approved": [
            "Download your admission letter from the portal",
            "Pay the admission fee to confirm your seat",
            "Apply for hostel accommodation if needed",
            "Complete your onboarding tasks in the My Tasks section",
        ],
        "enrolled": [
            "Complete all remaining onboarding tasks",
            "Access your LMS portal for course materials",
            "Attend the orientation program",
            "Connect with your assigned faculty mentor",
        ],
    }
    return stage_map.get(user.admission_status.value, [
        "Visit the AI Admission section to start your application",
        "Ask Saarthi if you have any questions about the process",
    ])


@router.post("/direct", response_model=ChatResponse)
async def chat_direct_rag(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
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

    # Track conversation for direct RAG too
    conv = await conversation_service.get_or_create(
        session=session,
        user_id=current_user.id,
        conversation_id=request.conversation_id,
    )
    conv = await conversation_service.increment_turn(session, conv)

    return ChatResponse(
        answer=result.get("answer", ""),
        sources=sources,
        context_used=result.get("context_used", 0),
        intent="faq",
        confidence=1.0,
        error=result.get("error"),
        conversation_id=str(conv.id),
        turn_count=conv.turn_count,
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
