"""
Escalation Agent — handles situations where the AI cannot resolve the student's issue.

Triggers:
- Student explicitly asks for human help
- Supervisor detects frustration or repeated failures
- Other agents flag should_escalate=True

This agent creates a support ticket in the database and informs the student.
"""

import uuid
from app.agents.state import AgentState
from app.models.ticket import SupportTicket, TicketPriority, TicketStatus
from app.database import async_session


async def escalation_node(state: AgentState) -> dict:
    """
    Escalation agent node.
    Creates a support ticket and returns a helpful message to the student.
    """
    user_message = state["user_message"]
    user_id = state.get("user_id", "")
    escalation_reason = state.get("escalation_reason", "")
    turn_count = state.get("turn_count", 0)

    # Determine priority based on context
    priority = TicketPriority.MEDIUM
    if turn_count > 3:
        priority = TicketPriority.HIGH
    if any(word in user_message.lower() for word in ["urgent", "emergency", "asap", "immediately"]):
        priority = TicketPriority.URGENT

    # Determine department from context
    department = _detect_department(user_message)

    # Create support ticket
    ticket_id = None
    try:
        uid = uuid.UUID(user_id)
        async with async_session() as session:
            ticket = SupportTicket(
                user_id=uid,
                subject=_generate_subject(user_message),
                description=(
                    f"Student message: {user_message}\n\n"
                    f"Escalation reason: {escalation_reason or 'Student requested human assistance'}\n"
                    f"Conversation turns before escalation: {turn_count}"
                ),
                priority=priority,
                status=TicketStatus.OPEN,
                department=department,
                source="ai_escalation",
            )
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)
            ticket_id = str(ticket.id)
    except Exception as e:
        return {
            "response": (
                "I understand you need more help than I can provide right now. "
                "Unfortunately, I wasn't able to create a support ticket automatically. "
                "Please contact the admin office directly or email the helpdesk. "
                "I apologize for the inconvenience."
            ),
            "error": f"Escalation ticket creation failed: {str(e)[:200]}",
            "messages": [{
                "role": "system",
                "content": f"Escalation agent: Failed to create ticket — {str(e)[:100]}",
                "agent": "escalation",
                "metadata": {"error": str(e)},
            }],
        }

    # Build response
    response = (
        f"I've created a support ticket for you so our team can help.\n\n"
        f"📋 **Ticket Details:**\n"
        f"- **Ticket ID:** `{ticket_id[:8]}...`\n"
        f"- **Priority:** {priority.value.capitalize()}\n"
        f"- **Department:** {department or 'General'}\n"
        f"- **Status:** Open\n\n"
        f"A member of our team will review your request and get back to you. "
        f"You can track your ticket status through the student portal.\n\n"
        f"In the meantime, is there anything else I can help you with?"
    )

    return {
        "response": response,
        "should_escalate": False,  # Reset after handling
        "messages": [{
            "role": "assistant",
            "content": f"Escalation agent: Created ticket {ticket_id[:8] if ticket_id else 'unknown'}",
            "agent": "escalation",
            "metadata": {
                "ticket_id": ticket_id,
                "priority": priority.value,
                "department": department,
            },
        }],
    }


def _generate_subject(message: str) -> str:
    """Generate a concise ticket subject from the student's message."""
    # Truncate to first sentence or 80 chars
    subject = message.strip()
    if "." in subject:
        subject = subject.split(".")[0]
    if len(subject) > 80:
        subject = subject[:77] + "..."
    return f"[AI Escalation] {subject}"


def _detect_department(message: str) -> str:
    """Simple keyword-based department detection."""
    msg = message.lower()

    if any(w in msg for w in ["fee", "payment", "scholarship", "installment", "refund"]):
        return "Accounts"
    elif any(w in msg for w in ["hostel", "room", "mess", "warden"]):
        return "Hostel"
    elif any(w in msg for w in ["exam", "result", "grade", "marks", "backlog"]):
        return "Examination"
    elif any(w in msg for w in ["admission", "document", "certificate", "marksheet"]):
        return "Admissions"
    elif any(w in msg for w in ["lms", "login", "password", "portal", "email", "it "]):
        return "IT Support"
    elif any(w in msg for w in ["branch", "subject", "elective", "timetable", "attendance"]):
        return "Academic"
    else:
        return "General"
