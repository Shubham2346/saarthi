"""
LangGraph State Graph — orchestrates the multi-agent system.

Graph Structure:
    ┌─────────────┐
    │   START     │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Supervisor │  (classifies intent)
    └──────┬──────┘
           │
     ┌─────┼─────┬──────────┬────────────┐
     │     │     │          │            │
  greeting faq  task    admission  escalation
     │     │     │          │            │
     └─────┴─────┴──────────┴────────────┘
           │
    ┌──────▼──────┐
    │     END     │
    └─────────────┘

Conditional routing happens after the Supervisor node based on the
classified intent. Each specialized agent processes the request
and writes its response to the shared state.
"""

from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.supervisor import supervisor_node
from app.agents.faq_agent import faq_node
from app.agents.task_agent import task_node
from app.agents.escalation_agent import escalation_node
from app.agents.greeting_handler import greeting_node
from app.agents.admission_agent import admission_node
from app.agents.document_verification_agent import document_verification_node


def _route_by_intent(state: AgentState) -> str:
    """
    Conditional edge function — routes to the appropriate agent
    based on the intent classified by the Supervisor.
    """
    intent = state.get("intent", "faq")
    should_escalate = state.get("should_escalate", False)

    # Override: if any previous node flagged escalation, go there
    if should_escalate:
        return "escalation"

    # Route based on supervisor classification
    routing_map = {
        "greeting": "greeting",
        "faq": "faq",
        "task": "task",
        "admission": "admission",
        "document": "document",
        "escalation": "escalation",
    }

    return routing_map.get(intent, "faq")  # Default to FAQ


def create_agent_graph() -> StateGraph:
    """
    Build and compile the LangGraph state graph.
    Returns a compiled graph ready to be invoked.
    """
    # Create the graph with our state schema
    graph = StateGraph(AgentState)

    # --- Add Nodes ---
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("greeting", greeting_node)
    graph.add_node("faq", faq_node)
    graph.add_node("task", task_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("admission", admission_node)
    graph.add_node("document", document_verification_node)

    # --- Add Edges ---

    # START → Supervisor (always the entry point)
    graph.set_entry_point("supervisor")

    # Supervisor → conditional routing based on intent
    graph.add_conditional_edges(
        "supervisor",
        _route_by_intent,
        {
            "greeting": "greeting",
            "faq": "faq",
            "task": "task",
            "admission": "admission",
            "document": "document",
            "escalation": "escalation",
        },
    )

    # All specialized agents → END (single-turn for now)
    graph.add_edge("greeting", END)
    graph.add_edge("faq", END)
    graph.add_edge("task", END)
    graph.add_edge("escalation", END)
    graph.add_edge("admission", END)
    graph.add_edge("document", END)

    # Compile the graph
    return graph.compile()


# Compiled graph singleton (bump GRAPH_BUILD_ID when graph topology changes)
GRAPH_BUILD_ID = 2
_compiled_graph: tuple[int, object] | None = None


def get_agent_graph():
    global _compiled_graph
    if _compiled_graph is None or _compiled_graph[0] != GRAPH_BUILD_ID:
        _compiled_graph = (GRAPH_BUILD_ID, create_agent_graph())
    return _compiled_graph[1]


async def run_agent(
    user_message: str,
    user_id: str,
    conversation_id: str = "",
    session_id: str = "",
    turn_count: int = 0,
    student_name: str = "",
    student_email: str = "",
) -> dict:
    """
    Run the multi-agent graph for a student's message.

    Args:
        user_message: The student's input text.
        user_id: The authenticated student's UUID string.
        conversation_id: Unique ID for this conversation.
        session_id: Current session identifier.
        turn_count: Current conversation turn number.
        student_name: Student's full name.
        student_email: Student's email address.

    Returns:
        Dict with 'response', 'intent', 'sources', 'context', etc.
    """
    import uuid as uuid_mod
    from datetime import datetime, timezone

    graph = get_agent_graph()

    now_iso = datetime.now(timezone.utc).isoformat()
    conv_id = conversation_id or str(uuid_mod.uuid4())

    # Initialize state with all AgentState TypedDict fields
    initial_state: AgentState = {
        "conversation_id": conv_id,
        "student_id": user_id,
        "session_id": session_id or conv_id,
        "user_message": user_message,
        "messages": [{
            "role": "user",
            "content": user_message,
            "agent": None,
            "timestamp": now_iso,
            "metadata": None,
        }],
        "current_phase": "initial_query",
        "turn_count": turn_count,
        "interaction_count": turn_count,
        "student_name": student_name or None,
        "student_email": student_email or None,
        "student_phone": None,
        "admitted_program": None,
        "admission_status": "pending",
        "current_agent": None,
        "supervisor_routing_decision": None,
        "intent": "",
        "query_category": None,
        "confidence": 0.0,
        "agent_sequence": [],
        "response": "",
        "agent_responses": [],
        "reasoning": None,
        "pending_tasks": [],
        "completed_tasks": [],
        "task_completion_percentage": 0.0,
        "next_priority_task": None,
        "uploaded_documents": [],
        "pending_document_approvals": [],
        "document_verification_results": None,
        "rag_search_query": None,
        "rag_search_results": [],
        "relevant_faq_ids": [],
        "sources": [],
        "should_escalate": False,
        "escalation_reason": None,
        "escalation_ticket_id": None,
        "error": None,
        "error_count": 0,
        "context": {},
        "conversation_start_time": now_iso,
        "last_updated": now_iso,
        "enable_debug": False,
        "verbose_logging": False,
    }

    # Run the graph
    try:
        result = await graph.ainvoke(initial_state)

        return {
            "response": result.get("response", "I'm sorry, I couldn't process your request."),
            "intent": result.get("intent", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "sources": result.get("sources", []),
            "context": result.get("context", {}),
            "messages": result.get("messages", []),
            "error": result.get("error", ""),
        }

    except Exception as e:
        return {
            "response": (
                "I encountered an unexpected error while processing your request. "
                "Please try again, or contact the admin office for immediate assistance."
            ),
            "intent": "error",
            "confidence": 0.0,
            "sources": [],
            "context": {},
            "messages": [],
            "error": f"Graph execution error: {str(e)}",
        }
