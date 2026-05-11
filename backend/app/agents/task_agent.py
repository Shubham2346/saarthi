"""
Task Agent — manages the student's onboarding checklist.

This agent queries the database for the student's pending tasks,
progress, and deadlines, then uses Ollama to generate a helpful,
personalized summary.

Tools available to this agent:
- get_pending_tasks: Fetch student's task list from DB
- get_progress: Calculate onboarding completion percentage
- get_deadlines: List upcoming deadlines
"""

import uuid
from datetime import datetime
from app.agents.state import AgentState
from app.services.ollama_service import ollama_service
from app.services.task_service import get_user_tasks, get_onboarding_progress
from app.database import async_session


TASK_AGENT_SYSTEM_PROMPT = """You are the **Task Agent** of Saarthi, a student onboarding assistant.

Your job is to help students understand their onboarding checklist — what they've done, what's pending, and what's urgent.

You will receive the student's TASK DATA (from the database) and their QUESTION.

Rules:
- Be encouraging and supportive. Celebrate completed tasks!
- Clearly list pending tasks with deadlines when relevant.
- If a task is overdue, flag it prominently but don't be harsh.
- If the student asks what to do next, recommend the highest-priority pending task.
- Format your response clearly with bullet points or numbered lists.
- Keep responses concise — 2-3 paragraphs max.
- Never make up tasks that aren't in the data. Only reference actual tasks provided."""


async def _fetch_task_data(user_id: str) -> dict:
    """Fetch the student's task data from the database."""
    try:
        uid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        return {"error": "Invalid user ID", "tasks": [], "progress": {}}

    try:
        async with async_session() as session:
            # Get all tasks with details
            user_tasks = await get_user_tasks(session, uid)

            # Get progress summary
            progress = await get_onboarding_progress(session, uid)

            # Format tasks for the LLM
            task_list = []
            for ut in user_tasks:
                task_info = {
                    "title": ut.task.title if ut.task else "Unknown Task",
                    "description": ut.task.description if ut.task else "",
                    "category": ut.task.category.value if ut.task else "general",
                    "status": ut.status.value,
                    "is_mandatory": ut.task.is_mandatory if ut.task else True,
                    "requires_document": ut.task.requires_document if ut.task else False,
                    "deadline": ut.task.deadline.strftime("%B %d, %Y") if ut.task and ut.task.deadline else "No deadline",
                    "completed_at": ut.completed_at.strftime("%B %d, %Y") if ut.completed_at else None,
                    "notes": ut.notes,
                }
                task_list.append(task_info)

            return {
                "tasks": task_list,
                "progress": progress,
            }
    except Exception as e:
        return {"error": str(e), "tasks": [], "progress": {}}


async def task_node(state: AgentState) -> dict:
    """
    Onboarding Task agent node.
    Fetches the student's tasks from the DB and generates a contextual response.
    """
    user_message = state["user_message"]
    user_id = state.get("user_id", "")

    # Fetch task data from database
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

    # Build the context prompt
    progress = task_data["progress"]
    tasks = task_data["tasks"]

    # Separate by status
    pending = [t for t in tasks if t["status"] == "pending"]
    in_progress = [t for t in tasks if t["status"] == "in_progress"]
    completed = [t for t in tasks if t["status"] == "completed"]
    overdue = [t for t in tasks if t["status"] == "overdue"]

    task_summary = f"""STUDENT'S ONBOARDING DATA:

Progress: {progress.get('completed', 0)}/{progress.get('total', 0)} tasks completed ({progress.get('percentage', 0)}%)

PENDING TASKS ({len(pending)}):
{chr(10).join(f'- {t["title"]} (Category: {t["category"]}, Deadline: {t["deadline"]}, Mandatory: {t["is_mandatory"]}, Needs Document: {t["requires_document"]})' for t in pending) if pending else '- None! All caught up!'}

IN PROGRESS ({len(in_progress)}):
{chr(10).join(f'- {t["title"]} (Deadline: {t["deadline"]})' for t in in_progress) if in_progress else '- None'}

COMPLETED ({len(completed)}):
{chr(10).join(f'- {t["title"]} (Completed: {t["completed_at"]})' for t in completed) if completed else '- None yet'}

OVERDUE ({len(overdue)}):
{chr(10).join(f'- ⚠️ {t["title"]} (Deadline was: {t["deadline"]})' for t in overdue) if overdue else '- None! Good job!'}
"""

    augmented_prompt = f"""{task_summary}

---

STUDENT'S QUESTION: {user_message}

Respond helpfully based on the task data above."""

    try:
        answer = await ollama_service.generate(
            prompt=augmented_prompt,
            system_prompt=TASK_AGENT_SYSTEM_PROMPT,
            temperature=0.5,
            max_tokens=800,
        )

        return {
            "response": answer,
            "context": {
                "progress": progress,
                "pending_count": len(pending),
                "overdue_count": len(overdue),
            },
            "messages": [{
                "role": "assistant",
                "content": f"Task agent: {progress.get('percentage', 0)}% complete, {len(pending)} pending, {len(overdue)} overdue",
                "agent": "task",
                "metadata": {"progress": progress},
            }],
        }

    except Exception as e:
        # Fallback: provide raw task data without LLM formatting
        fallback = _format_tasks_fallback(pending, completed, overdue, progress)
        return {
            "response": fallback,
            "context": {"progress": progress},
            "error": f"Task agent LLM error (fallback used): {str(e)[:200]}",
            "messages": [{
                "role": "system",
                "content": f"Task agent: LLM failed, using fallback. Error: {str(e)[:100]}",
                "agent": "task",
                "metadata": {"error": str(e), "used_fallback": True},
            }],
        }


def _format_tasks_fallback(pending, completed, overdue, progress) -> str:
    """Plain-text fallback when the LLM is unavailable."""
    lines = [f"📋 **Your Onboarding Progress: {progress.get('percentage', 0)}%**\n"]

    if overdue:
        lines.append("⚠️ **Overdue Tasks:**")
        for t in overdue:
            lines.append(f"  - {t['title']} (Deadline was: {t['deadline']})")
        lines.append("")

    if pending:
        lines.append("📌 **Pending Tasks:**")
        for t in pending:
            mandatory = " *(Required)*" if t["is_mandatory"] else " *(Optional)*"
            lines.append(f"  - {t['title']}{mandatory} — Due: {t['deadline']}")
        lines.append("")

    if completed:
        lines.append(f"✅ **Completed: {len(completed)} tasks**")

    if not pending and not overdue:
        lines.append("🎉 All tasks are complete! You're all set for onboarding!")

    return "\n".join(lines)
