"""
Comprehensive Agent State Management for LangGraph Multi-Agent System

This module defines the centralized state that flows through the agent graph.
All agents work with this unified state, ensuring consistency and proper
information flow through the conversation.

PHASE 3 ENHANCEMENT:
- Complete TypedDict for LangGraph compatibility
- Annotated reducers for proper state merging
- Support for multi-turn conversations
- Agent routing and escalation tracking
"""

from __future__ import annotations

import operator
import uuid
from datetime import datetime
from typing import Any, Annotated, Dict, List, Optional
from typing_extensions import TypedDict
from enum import Enum


class AgentType(Enum):
    """Enum for different agent types in the system."""
    SUPERVISOR = "supervisor"
    TASK_AGENT = "task_agent"
    DOCUMENT_VERIFICATION = "document_verification"
    FAQ_AGENT = "faq_agent"
    ADMISSION_AGENT = "admission_agent"
    GREETING_AGENT = "greeting_agent"
    ESCALATION_AGENT = "escalation_agent"


class ConversationPhase(Enum):
    """Enum for conversation phases/stages."""
    GREETING = "greeting"
    INITIAL_QUERY = "initial_query"
    PROCESSING = "processing"
    CLARIFICATION = "clarification"
    RESOLUTION = "resolution"
    ESCALATION = "escalation"


class DocumentStatus(Enum):
    """Status of uploaded documents."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class TaskStatus(Enum):
    """Status of onboarding tasks."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class AgentMessage(TypedDict):
    """A single message in the conversation history."""
    role: str  # "user", "assistant", "system", "tool", "agent"
    content: str
    agent: Optional[str]  # which agent generated this message
    timestamp: str  # ISO format datetime
    metadata: Optional[Dict[str, Any]]


class AgentState(TypedDict):
    """
    Comprehensive shared state that flows through the entire LangGraph.

    This state object is passed between all agents and ensures:
    1. Consistency across agent interactions
    2. Proper context maintenance
    3. State history for debugging/analytics
    4. Escalation tracking
    5. Document and task management

    Fields are organized by functional area for clarity.
    """
    
    # =========================================================================
    # CORE IDENTIFIERS
    # =========================================================================
    
    conversation_id: str  # Unique ID for this conversation
    student_id: str  # The authenticated student's UUID
    session_id: str  # Current session identifier
    
    # =========================================================================
    # CONVERSATION STATE
    # =========================================================================
    
    user_message: str  # Current message from the student
    messages: Annotated[List[AgentMessage], operator.add]  # Full history
    current_phase: str  # Current phase: greeting, initial_query, processing, etc.
    turn_count: int  # Number of conversation turns
    interaction_count: int  # Total interactions in this conversation
    
    # =========================================================================
    # STUDENT INFORMATION
    # =========================================================================
    
    student_name: Optional[str]
    student_email: Optional[str]
    student_phone: Optional[str]
    admitted_program: Optional[str]
    admission_status: str  # pending, admitted, rejected, enrolled
    
    # =========================================================================
    # AGENT ROUTING & ORCHESTRATION
    # =========================================================================
    
    current_agent: Optional[str]  # Which agent is currently processing
    supervisor_routing_decision: Optional[str]  # Where supervisor routed to
    intent: str  # Classified intent from supervisor
    query_category: Optional[str]  # Categorization: task, document, faq, escalation
    confidence: float  # How confident supervisor is (0-1)
    agent_sequence: Annotated[List[str], operator.add]  # History of agents used
    
    # =========================================================================
    # RESPONSE & OUTPUT
    # =========================================================================
    
    response: str  # The final response to send to student
    agent_responses: Annotated[List[Dict[str, Any]], operator.add]  # Responses from all agents
    reasoning: Optional[str]  # Explanation of how response was generated
    
    # =========================================================================
    # TASK MANAGEMENT
    # =========================================================================
    
    pending_tasks: List[Dict[str, Any]]  # Tasks awaiting completion
    completed_tasks: Annotated[List[Dict[str, Any]], operator.add]  # Completed tasks
    task_completion_percentage: float  # Percentage of tasks completed
    next_priority_task: Optional[Dict[str, Any]]  # Most urgent pending task
    
    # =========================================================================
    # DOCUMENT TRACKING
    # =========================================================================
    
    uploaded_documents: Annotated[List[Dict[str, Any]], operator.add]  # All docs
    pending_document_approvals: List[Dict[str, Any]]  # Docs waiting for approval
    document_verification_results: Optional[Dict[str, Any]]  # OCR results
    
    # =========================================================================
    # RAG & KNOWLEDGE BASE
    # =========================================================================
    
    rag_search_query: Optional[str]  # RAG search that was performed
    rag_search_results: Annotated[List[Dict[str, Any]], operator.add]  # RAG hits
    relevant_faq_ids: List[str]  # Relevant FAQ item IDs
    sources: Annotated[List[str], operator.add]  # Sources used in response
    
    # =========================================================================
    # ESCALATION & ERROR HANDLING
    # =========================================================================
    
    should_escalate: bool  # Flag to escalate to human
    escalation_reason: Optional[str]  # Why escalation was triggered
    escalation_ticket_id: Optional[str]  # Support ticket created
    error: Optional[str]  # Any error that occurred
    error_count: int  # Number of errors in this conversation
    context: Dict[str, Any]  # Additional context from agents
    
    # =========================================================================
    # METADATA & ANALYTICS
    # =========================================================================
    
    conversation_start_time: str  # ISO format
    last_updated: str  # ISO format
    enable_debug: bool  # Enable debug logging
    verbose_logging: bool  # Enable verbose output
