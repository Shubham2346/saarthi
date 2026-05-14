"""
Chat request/response schemas for the RAG-powered FAQ agent.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Student's chat message to the FAQ agent."""
    message: str
    category: Optional[str] = None  # Optional filter: admission, fee, hostel, etc.
    stream: bool = False  # Whether to stream the response via SSE
    conversation_id: Optional[str] = None  # Existing conversation to continue


class ChatSource(BaseModel):
    """A source document used to generate the answer."""
    question: str
    category: str
    relevance_score: float


class AgentTraceMessage(BaseModel):
    """A trace message from an agent in the multi-agent pipeline."""
    agent: str
    content: str


class ChatResponse(BaseModel):
    """Response from the multi-agent system."""
    answer: str
    sources: List[ChatSource] = []
    context_used: int = 0
    intent: Optional[str] = None  # Classified intent: faq, task, escalation, greeting
    confidence: Optional[float] = None  # Supervisor's confidence in classification
    agent_messages: List[AgentTraceMessage] = []  # Trace of agent processing
    error: Optional[str] = None
    admission_application: Optional[Dict[str, Any]] = None
    admission_pipeline_percent: Optional[int] = None
    admission_fields_updated: Optional[List[str]] = None
    conversation_id: Optional[str] = None
    turn_count: int = 0
    user_role: Optional[str] = None
    user_admission_status: Optional[str] = None
    user_onboarding_stage: Optional[str] = None
    suggested_next_steps: Optional[List[str]] = None


class KnowledgeSearchRequest(BaseModel):
    """Search the knowledge base directly (admin/debug tool)."""
    query: str
    category: Optional[str] = None
    n_results: int = 10


class KnowledgeSearchResult(BaseModel):
    """A single search result from the knowledge base."""
    id: str
    question: str
    answer: str
    category: str
    relevance_score: float
