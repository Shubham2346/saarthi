"""
Task Agent — manages the student's onboarding checklist using template-based responses.
No LLM/Ollama dependency. All responses are built from database data directly.
"""

import uuid
from datetime import datetime
from app.agents.state import AgentState
from app.services.task_service import get_user_tasks, get_onboarding_progress
from app.database import async_session


async def _fetch_task_data(user_id: str) -> dict:
    """Fetch the student's task data from the database."""
    try:
        uid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        return {"error": "Invalid user ID", "tasks": [], "progress": {}}

    try:
        async with async_session() as session:
            user_tasks = await get_user_tasks(session, uid)
            progress = await get_onboarding_progress(session, uid)

            task_list = []
            for ut in user_tasks:
                task_info = {
                    "title": ut.task.title if ut.task else "Unknown Task",
                    "description": ut.task.description if ut.task else "",
                    "category": ut.task.category.value if ut.task else "general",
                    "status": ut.status.value,
                    "is_mandatory": ut.task.is_mandatory if ut.task else True,
                    "requires_document": ut.task.requires_document if ut.task else False,
                    "deadline": (
                        ut.task.deadline.strftime("%B %d, %Y")
                        if ut.task and ut.task.deadline
                        else "No deadline"
                    ),
                    "completed_at": (
                        ut.completed_at.strftime("%B %d, %Y")
                        if ut.completed_at
                        else None
                    ),
                    "notes": ut.notes,
                }
                task_list.append(task_info)

            return {"tasks": task_list, "progress": progress}
    except Exception as e:
        return {"error": str(e), "tasks": [], "progress": {}}


def _format_tasks_response(task_data: dict, user_message: str) -> str:
    """Build a structured response from task data without LLM."""
    progress = task_data.get("progress", {})
    tasks = task_data.get("tasks", [])

    pending = [t for t in tasks if t["status"] == "pending"]
    in_progress = [t for t in tasks if t["status"] == "in_progress"]
    completed = [t for t in tasks if t["status"] == "completed"]
    overdue = [t for t in tasks if t["status"] == "overdue"]

    total = progress.get("total", 0)
    completed_count = progress.get("completed", 0)
    percentage = progress.get("percentage", 0)

    q_lower = user_message.lower()

    lines = []

    if any(w in q_lower for w in ["progress", "status", "how am i doing", "complete"]):
        lines.append(f"Your onboarding progress is {percentage}% complete.")
        lines.append(f"You have completed {completed_count} out of {total} tasks.")
        if overdue:
            lines.append(f"You have {len(overdue)} overdue task(s) that need immediate attention.")
        if pending:
            lines.append(f"You have {len(pending)} pending task(s) ahead of you.")
        lines.append("")

    if any(w in q_lower for w in ["next", "what to do", "what should i", "todo", "pending", "remaining"]):
        if overdue:
            lines.append("IMPORTANT — Overdue tasks (complete these first):")
            for t in overdue:
                lines.append(f"  - {t['title']} (was due: {t['deadline']})")
            lines.append("")

        if pending:
            if not lines:
                lines.append("Here are your next steps:")
            for t in pending[:5]:
                mandatory = "(Required)" if t["is_mandatory"] else "(Optional)"
                lines.append(f"  - {t['title']} {mandatory} — Due: {t['deadline']}")
                if t["requires_document"]:
                    lines.append(f"    (you need to upload a document for this)")
            if pending and not overdue:
                lines.append(
                    "\nTip: Focus on the mandatory tasks first, then complete the optional ones."
                )
        elif not overdue and not pending:
            lines.append("All tasks are complete! You're all set for onboarding.")
            lines.append("If you need help with anything else, just ask!")

    if any(w in q_lower for w in ["all", "list", "show", "view", "tasks", "what are"]):
        if total == 0:
            lines.append("You don't have any onboarding tasks assigned yet. Please contact the admin.")
        else:
            if overdue:
                lines.append(f"Overdue ({len(overdue)}):")
                for t in overdue:
                    lines.append(f"  - {t['title']} (due was {t['deadline']})")
            if pending:
                lines.append(f"Pending ({len(pending)}):")
                for t in pending:
                    lines.append(f"  - {t['title']} (Due: {t['deadline']})")
            if in_progress:
                lines.append(f"In Progress ({len(in_progress)}):")
                for t in in_progress:
                    lines.append(f"  - {t['title']} (Due: {t['deadline']})")
            if completed:
                lines.append(f"Completed ({len(completed)}):")
                for t in completed:
                    lines.append(f"  - {t['title']} (on {t['completed_at']})")

    if any(w in q_lower for w in ["deadline", "due", "urgent", "overdue", "when"]):
        if overdue:
            lines.append("Overdue tasks: You should complete these right away!")
            for t in overdue:
                lines.append(f"  - {t['title']} (was due: {t['deadline']})")
        if pending and any(t["deadline"] != "No deadline" for t in pending):
            lines.append("Upcoming deadlines:")
            sorted_pending = sorted(
                [t for t in pending if t["deadline"] != "No deadline"],
                key=lambda t: t["deadline"],
            )
            for t in sorted_pending[:5]:
                lines.append(f"  - {t['title']} (Due: {t['deadline']})")
        if not pending and not overdue:
            lines.append("You have no upcoming deadlines. All tasks are complete!")

    if not lines:
        lines.append(f"Here's a summary of your onboarding tasks:")
        lines.append(f"You're {percentage}% done ({completed_count}/{total} tasks).")
        if overdue:
            lines.append(f"You have {len(overdue)} overdue and {len(pending)} pending tasks.")
        elif pending:
            lines.append(f"You have {len(pending)} pending tasks remaining.")
        else:
            lines.append("All done! Great job.")
        lines.append("\nVisit the 'My Tasks' section for full details.")

    return "\n".join(lines)


async def task_node(state: AgentState) -> dict:
    """
    Onboarding Task agent node.
    Fetches the student's tasks from the DB and builds a structured response.
    No LLM/Ollama usage.
    """
    user_message = state["user_message"]
    user_id = state.get("user_id", "")

    task_data = await _fetch_task_data(user_id)

    if task_data.get("error") and not task_data["tasks"]:
        return {
            "response": (
                "I wasn't able to fetch your onboarding tasks. This could mean "
                "your tasks haven't been assigned yet, or there's a temporary issue. "
                "Please try again or contact the admin office for help."
            ),
            "messages": [{
                "role": "system",
                "content": f"Task agent: DB error — {task_data.get('error', 'unknown')[:100]}",
                "agent": "task",
                "metadata": {"error": task_data.get("error")},
            }],
        }

    progress = task_data.get("progress", {})
    tasks = task_data.get("tasks", [])
    pending = [t for t in tasks if t["status"] == "pending"]
    overdue = [t for t in tasks if t["status"] == "overdue"]

    answer = _format_tasks_response(task_data, user_message)

    return {
        "response": answer,
        "context": {
            "progress": progress,
            "pending_count": len(pending),
            "overdue_count": len(overdue),
        },
        "messages": [{
            "role": "assistant",
            "content": (
                f"Task agent: {progress.get('percentage', 0)}% complete, "
                f"{len(pending)} pending, {len(overdue)} overdue"
            ),
            "agent": "task",
            "metadata": {"progress": progress},
        }],
    }
