"""
Support tickets router — create, list, update, and manage helpdesk tickets.
"""

import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.schemas.ticket import (
    SupportTicketCreate,
    SupportTicketRead,
    SupportTicketUpdate,
)
from app.middleware.auth import get_current_user, require_admin, require_admin_or_mentor
from app.models.user import User
from app.models.ticket import SupportTicket, TicketStatus

router = APIRouter(prefix="/tickets", tags=["Support Tickets"])


@router.post("/", response_model=SupportTicketRead, status_code=201)
async def create_ticket(
    ticket: SupportTicketCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new support ticket."""
    new_ticket = SupportTicket(
        user_id=current_user.id,
        subject=ticket.subject,
        description=ticket.description,
        priority=ticket.priority,
        department=ticket.department,
        source="manual",
    )
    session.add(new_ticket)
    await session.flush()
    return SupportTicketRead.model_validate(new_ticket)


@router.get("/my-tickets", response_model=List[SupportTicketRead])
async def list_my_tickets(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List all tickets created by the current user."""
    statement = (
        select(SupportTicket)
        .where(SupportTicket.user_id == current_user.id)
        .order_by(SupportTicket.created_at.desc())
    )
    result = await session.execute(statement)
    tickets = result.scalars().all()
    return [SupportTicketRead.model_validate(t) for t in tickets]


@router.get("/", response_model=List[SupportTicketRead])
async def list_all_tickets(
    status_filter: Optional[str] = Query(default=None, alias="status"),
    department: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    _staff: User = Depends(require_admin_or_mentor),
):
    """List all tickets (admin/mentor only). Optionally filter by status or department."""
    statement = select(SupportTicket)

    if status_filter:
        statement = statement.where(SupportTicket.status == status_filter)
    if department:
        statement = statement.where(SupportTicket.department == department)

    statement = statement.order_by(SupportTicket.created_at.desc())
    result = await session.execute(statement)
    tickets = result.scalars().all()
    return [SupportTicketRead.model_validate(t) for t in tickets]


@router.get("/{ticket_id}", response_model=SupportTicketRead)
async def get_ticket(
    ticket_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get details of a specific ticket."""
    statement = select(SupportTicket).where(SupportTicket.id == ticket_id)
    result = await session.execute(statement)
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Students can only view their own tickets
    if current_user.role == "student" and ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return SupportTicketRead.model_validate(ticket)


@router.patch("/{ticket_id}", response_model=SupportTicketRead)
async def update_ticket(
    ticket_id: uuid.UUID,
    update: SupportTicketUpdate,
    session: AsyncSession = Depends(get_session),
    _staff: User = Depends(require_admin_or_mentor),
):
    """Update a ticket (admin/mentor only) — assign, resolve, change priority, etc."""
    statement = select(SupportTicket).where(SupportTicket.id == ticket_id)
    result = await session.execute(statement)
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)

    # Auto-set resolved_at when status changes to resolved
    if update_data.get("status") in (TicketStatus.RESOLVED, TicketStatus.CLOSED):
        ticket.resolved_at = datetime.utcnow()

    ticket.updated_at = datetime.utcnow()
    session.add(ticket)
    await session.flush()

    return SupportTicketRead.model_validate(ticket)


@router.get("/stats/summary")
async def get_ticket_stats(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get summary statistics for support tickets (admin only)."""
    statement = select(SupportTicket)
    result = await session.execute(statement)
    tickets = result.scalars().all()

    total = len(tickets)
    open_count = sum(1 for t in tickets if t.status == TicketStatus.OPEN)
    assigned = sum(1 for t in tickets if t.status == TicketStatus.ASSIGNED)
    in_progress = sum(1 for t in tickets if t.status == TicketStatus.IN_PROGRESS)
    resolved = sum(1 for t in tickets if t.status == TicketStatus.RESOLVED)
    closed = sum(1 for t in tickets if t.status == TicketStatus.CLOSED)

    return {
        "total": total,
        "open": open_count,
        "assigned": assigned,
        "in_progress": in_progress,
        "resolved": resolved,
        "closed": closed,
    }
