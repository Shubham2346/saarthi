import asyncio
import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, init_db
from app.models.user import User, UserRole
from app.agents.graph import run_agent

async def run_tests():
    print("Initializing Database...")
    await init_db()

    async with AsyncSession(engine) as session:
        # Create a mock student
        student_id = uuid.uuid4()
        student = User(
            id=student_id,
            email="test_student@example.com",
            full_name="Test Student",
            google_id="test_google_123",
            role=UserRole.STUDENT
        )
        session.add(student)
        
        # Create a mock mentor
        mentor_id = uuid.uuid4()
        mentor = User(
            id=mentor_id,
            email="test_mentor@example.com",
            full_name="Test Mentor",
            google_id="test_google_456",
            role=UserRole.MENTOR
        )
        session.add(mentor)
        await session.commit()
        
        print("\n--- Test 1: Mentor Assignment Workflow ---")
        result = await run_agent("Please assign me a mentor", str(student_id))
        print("Intent Detected:", result.get("intent"))
        print("Agent Response:", result.get("response"))
        
        # Verify in database
        updated_student = await session.get(User, student_id)
        print("Mentor Assigned in DB?", updated_student.mentor_id == mentor_id)
        
        print("\n--- Test 2: Hostel Application Workflow ---")
        result = await run_agent("I need to apply for a hostel room", str(student_id))
        print("Intent Detected:", result.get("intent"))
        print("Agent Response:", result.get("response"))
        
        # Cleanup
        await session.delete(updated_student)
        await session.delete(mentor)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(run_tests())
