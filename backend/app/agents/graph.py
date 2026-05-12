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
     ┌─────┼─────┬─────┬─────┐
     │     │     │     │     │
  greeting faq  task  doc escalation
     │     │     │     │     │
     └─────┼─────┴─────┴─────┘
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
from app.agents.document_agent import document_node
from app.agents.escalation_agent import escalation_node
from app.agents.greeting_handler import greeting_node


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
    graph.add_node("document", document_node)
    graph.add_node("escalation", escalation_node)

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
            "document": "document",
            "escalation": "escalation",
        },
    )

    # All specialized agents → END (single-turn for now)
    graph.add_edge("greeting", END)
    graph.add_edge("faq", END)
    graph.add_edge("task", END)
    graph.add_edge("document", END)
    graph.add_edge("escalation", END)

    # Compile the graph
    return graph.compile()


# Create a singleton compiled graph
_compiled_graph = None


def get_agent_graph():
    """Get or create the singleton compiled graph."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = create_agent_graph()
    return _compiled_graph


async def run_agent(
    user_message: str,
    user_id: str,
    turn_count: int = 0,
) -> dict:
    """
    Run the multi-agent graph for a student's message.

    Args:
        user_message: The student's input text.
        user_id: The authenticated student's UUID string.
        turn_count: Current conversation turn number.

    Returns:
        Dict with 'response', 'intent', 'sources', 'context', etc.
    """
    graph = get_agent_graph()

    # Initialize state
    initial_state: AgentState = {
        "user_id": user_id,
        "user_message": user_message,
        "messages": [{
            "role": "user",
            "content": user_message,
            "agent": None,
            "metadata": None,
        }],
        "intent": "",
        "confidence": 0.0,
        "response": "",
        "sources": [],
        "context": {},
        "should_escalate": False,
        "escalation_reason": "",
        "error": "",
        "turn_count": turn_count,
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
