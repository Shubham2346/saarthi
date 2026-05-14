import json
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import engine
from app.agents.state import AgentState
from app.models.user import User, UserRole
from app.models.hostel import HostelAllocation, AllocationStatus
from app.services.ollama_service import ollama_service

WORKFLOW_SYSTEM_PROMPT = """You are the Workflow Automation Agent for Saarthi.
Your job is to determine which internal system workflow the user wants to trigger based on their message.

Workflows available:
1. "mentor_assignment" - User is asking for a mentor, faculty advisor, or guide to be assigned.
2. "hostel_application" - User wants to apply for a hostel, dorm, or accommodation.

Respond with ONLY a JSON object:
{"workflow": "workflow_name"}

If no workflow matches, respond with {"workflow": "unknown"}.
"""

async def workflow_node(state: AgentState) -> dict:
    """
    Automates internal onboarding workflows using LangGraph and SQLAlchemy.
    """
    user_message = state["user_message"]
    user_id = uuid.UUID(state["user_id"])

    # 1. Ask LLM which workflow to trigger
    try:
        raw_response = await ollama_service.generate(
            prompt=f'User message: "{user_message}"',
            system_prompt=WORKFLOW_SYSTEM_PROMPT,
            temperature=0.1,
            max_tokens=50,
        )
        
        # Parse JSON
        import re
        json_match = re.search(r'\{[^}]+\}', raw_response)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"workflow": "unknown"}
            
    except Exception as e:
        result = {"workflow": "unknown"}

    workflow_type = result.get("workflow", "unknown")
    
    response_text = ""
    
    # 2. Execute the workflow autonomously
    async with AsyncSession(engine) as session:
        student = await session.get(User, user_id)
        
        if not student:
            response_text = "I couldn't find your profile to execute this workflow."
            
        elif workflow_type == "mentor_assignment":
            # Auto-assign a mentor
            if student.mentor_id:
                response_text = "You already have a mentor assigned to you. Check your dashboard."
            else:
                # Find any available mentor
                stmt = select(User).where(User.role == UserRole.MENTOR)
                mentors = (await session.execute(stmt)).scalars().all()
                if mentors:
                    # Assign the first available mentor (simple logic for now)
                    assigned_mentor = mentors[0]
                    student.mentor_id = assigned_mentor.id
                    session.add(student)
                    await session.commit()
                    response_text = f"Automated Workflow Complete: I have successfully assigned {assigned_mentor.full_name} as your faculty mentor. You can view their details in your dashboard."
                else:
                    response_text = "I tried to assign you a mentor automatically, but no mentors are currently registered in the system."
                    
        elif workflow_type == "hostel_application":
            # Auto-apply for hostel
            stmt = select(HostelAllocation).where(HostelAllocation.user_id == user_id)
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if existing:
                response_text = f"You have already applied for a hostel. Your current status is: {existing.status.value.upper()}."
            else:
                new_allocation = HostelAllocation(user_id=user_id, status=AllocationStatus.APPLIED)
                session.add(new_allocation)
                await session.commit()
                response_text = "Automated Workflow Complete: I have successfully submitted your hostel application. The admin staff will review it shortly."
                
        else:
            response_text = "I understand you want to perform an action, but I don't have an automated workflow configured for that specific request yet. Let me know if you want me to raise a support ticket instead."

    return {
        "response": response_text,
        "messages": [{
            "role": "assistant",
            "content": response_text,
            "agent": "workflow_agent",
            "metadata": {"workflow_executed": workflow_type}
        }]
    }
