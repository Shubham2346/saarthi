"""
Support Ticket model — handles escalated student issues.
Created manually or by the Escalation Agent in later phases.
"""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.user import User


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SupportTicket(SQLModel, table=True):
    """Helpdesk ticket for escalated or unresolved student queries."""

    __tablename__ = "support_tickets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

    subject: str = Field(max_length=255)
    description: str = Field()

    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM,
        sa_column=Column(
            SAEnum(TicketPriority),
            nullable=False,
            default=TicketPriority.MEDIUM,
        ),
    )
    status: TicketStatus = Field(
        default=TicketStatus.OPEN,
        sa_column=Column(
            SAEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN
        ),
    )

    department: Optional[str] = Field(default=None, max_length=100)
    assigned_to: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    resolution_notes: Optional[str] = Field(default=None)
    resolved_at: Optional[datetime] = Field(default=None)

    # Source — was this created manually or by the AI escalation agent?
    source: str = Field(default="manual", max_length=50)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="tickets_created",
        sa_relationship_kwargs={"foreign_keys": "[SupportTicket.user_id]"},
    )
