"""
Agent State — the shared state object that flows through the LangGraph.

Every node in the graph reads from and writes to this state.
LangGraph uses TypedDict + Annotated reducers to manage state updates.
"""

from __future__ import annotations

import uuid
from typing import Optional, List, Dict, Any, Annotated
from typing_extensions import TypedDict

# LangGraph uses `operator.add` as a reducer for list fields,
# meaning each node's output gets appended to the existing list.
import operator


class AgentMessage(TypedDict):
    """A single message in the conversation history."""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    agent: Optional[str]  # which agent generated this message
    metadata: Optional[Dict[str, Any]]


class AgentState(TypedDict):
    """
    The shared state that flows through the entire LangGraph.

    Fields:
        user_id: The authenticated student's UUID
        user_message: The current message from the student
        messages: Full conversation history (appended by each node)
        intent: Classified intent from the supervisor (faq, task, escalation, greeting)
        confidence: How confident the supervisor is in the classification
        response: The final response to send back to the student
        sources: RAG sources used (if any)
        context: Additional context gathered by agents
        should_escalate: Flag set by any agent if escalation is needed
        escalation_reason: Why escalation was triggered
        error: Any error that occurred during processing
        turn_count: Number of conversation turns (for escalation detection)
    """
    user_id: str
    user_message: str
    messages: Annotated[List[AgentMessage], operator.add]
    intent: str
    confidence: float
    response: str
    sources: List[Dict[str, Any]]
    context: Dict[str, Any]
    should_escalate: bool
    escalation_reason: str
    error: str
    turn_count: int
