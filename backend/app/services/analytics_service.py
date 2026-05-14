from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User, UserRole
from app.models.task import UserTask, TaskStatus
from app.models.document import Document, DocumentStatus
from app.models.ticket import SupportTicket, TicketStatus

async def get_dashboard_metrics(session: AsyncSession):
    # Total Users and Students
    total_users_query = await session.execute(select(func.count(User.id)))
    total_users = total_users_query.scalar_one()

    total_students_query = await session.execute(
        select(func.count(User.id)).where(User.role == UserRole.STUDENT)
    )
    total_students = total_students_query.scalar_one()

    # Task metrics
    total_tasks_query = await session.execute(select(func.count(UserTask.id)))
    total_tasks = total_tasks_query.scalar_one()

    completed_tasks_query = await session.execute(
        select(func.count(UserTask.id)).where(UserTask.status == TaskStatus.COMPLETED)
    )
    completed_tasks = completed_tasks_query.scalar_one()

    # Document metrics
    pending_docs_query = await session.execute(
        select(func.count(Document.id)).where(Document.status == DocumentStatus.PENDING)
    )
    pending_docs = pending_docs_query.scalar_one()

    verified_docs_query = await session.execute(
        select(func.count(Document.id)).where(Document.status == DocumentStatus.VERIFIED)
    )
    verified_docs = verified_docs_query.scalar_one()

    # Ticket metrics
    open_tickets_query = await session.execute(
        select(func.count(SupportTicket.id)).where(SupportTicket.status == TicketStatus.OPEN)
    )
    open_tickets = open_tickets_query.scalar_one()

    resolved_tickets_query = await session.execute(
        select(func.count(SupportTicket.id)).where(SupportTicket.status == TicketStatus.RESOLVED)
    )
    resolved_tickets = resolved_tickets_query.scalar_one()

    # Calculation
    task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        "users": {
            "total": total_users,
            "students": total_students,
        },
        "tasks": {
            "total_assigned": total_tasks,
            "completed": completed_tasks,
            "completion_rate": round(task_completion_rate, 2),
        },
        "documents": {
            "pending_verification": pending_docs,
            "verified": verified_docs,
        },
        "tickets": {
            "open": open_tickets,
            "resolved": resolved_tickets,
        }
    }
