"""
Support ticket request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.ticket import TicketPriority, TicketStatus


class SupportTicketCreate(BaseModel):
    """Create a new support ticket."""
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    department: Optional[str] = None


class SupportTicketRead(BaseModel):
    """Ticket data returned in API responses."""
    id: uuid.UUID
    user_id: uuid.UUID
    subject: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    department: Optional[str] = None
    assigned_to: Optional[uuid.UUID] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupportTicketUpdate(BaseModel):
    """Update ticket (admin: assign, resolve, close)."""
    status: Optional[TicketStatus] = None
    assigned_to: Optional[uuid.UUID] = None
    department: Optional[str] = None
    resolution_notes: Optional[str] = None
    priority: Optional[TicketPriority] = None
