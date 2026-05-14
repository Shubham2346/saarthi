"""
Database seed script — populates the database with default onboarding tasks
and an admin user for initial testing.

Usage:
    python -m app.seed
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta

from sqlmodel import select
from app.database import engine, async_session, init_db
from app.models.user import User, UserRole, OnboardingStage
from app.models.task import OnboardingTask, TaskCategory


# Default onboarding tasks for engineering college admissions
DEFAULT_TASKS = [
    {
        "title": "Upload 10th Marksheet",
        "description": "Upload a clear scan or photo of your 10th standard marksheet for verification.",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 1,
        "is_mandatory": True,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Upload 12th Marksheet",
        "description": "Upload a clear scan or photo of your 12th standard marksheet for verification.",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 2,
        "is_mandatory": True,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Upload Entrance Exam Scorecard",
        "description": "Upload your CET/JEE/NEET scorecard as applicable to your admission category.",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 3,
        "is_mandatory": True,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Upload Aadhaar Card",
        "description": "Upload a clear scan of your Aadhaar card (front and back).",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 4,
        "is_mandatory": True,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Upload Passport-Size Photo",
        "description": "Upload a recent passport-size photo with white background (JPEG/PNG).",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 5,
        "is_mandatory": True,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Upload Caste Certificate",
        "description": "Upload caste/category certificate if applicable (SC/ST/OBC/EWS).",
        "category": TaskCategory.DOCUMENT,
        "sort_order": 6,
        "is_mandatory": False,
        "requires_document": True,
        "deadline": datetime.utcnow() + timedelta(days=30),
    },
    {
        "title": "Pay Admission Fee",
        "description": "Complete the admission fee payment through the college payment portal.",
        "category": TaskCategory.FEE,
        "sort_order": 7,
        "is_mandatory": True,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=15),
    },
    {
        "title": "Pay Hostel Fee",
        "description": "If opting for hostel accommodation, complete the hostel fee payment.",
        "category": TaskCategory.FEE,
        "sort_order": 8,
        "is_mandatory": False,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=20),
    },
    {
        "title": "Fill Academic Preference Form",
        "description": "Select your preferred branch/specialization and elective subjects.",
        "category": TaskCategory.ACADEMIC,
        "sort_order": 9,
        "is_mandatory": True,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=25),
    },
    {
        "title": "Attend Orientation Session",
        "description": "Attend the mandatory orientation session (online or in-person as scheduled).",
        "category": TaskCategory.ORIENTATION,
        "sort_order": 10,
        "is_mandatory": True,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=40),
    },
    {
        "title": "Setup College Email & LMS Account",
        "description": "Activate your college email ID and login to the Learning Management System (LMS).",
        "category": TaskCategory.GENERAL,
        "sort_order": 11,
        "is_mandatory": True,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=35),
    },
    {
        "title": "Collect Student ID Card",
        "description": "Visit the admin office or designated center to collect your student ID card.",
        "category": TaskCategory.GENERAL,
        "sort_order": 12,
        "is_mandatory": True,
        "requires_document": False,
        "deadline": datetime.utcnow() + timedelta(days=45),
    },
]


async def seed_database():
    """Populate the database with default data."""
    await init_db()

    async with async_session() as session:
        # --- Seed Admin User ---
        existing_admin = await session.execute(
            select(User).where(User.email == "admin@saarthi.dev")
        )
        if not existing_admin.scalar_one_or_none():
            admin = User(
                email="admin@saarthi.dev",
                full_name="Saarthi Admin",
                google_id="admin-seed-account",
                role=UserRole.ADMIN,
                stage=OnboardingStage.COMPLETED,
            )
            session.add(admin)
            print("✅ Admin user created: admin@saarthi.dev")
        else:
            print("ℹ️  Admin user already exists")

        # --- Seed Onboarding Tasks ---
        existing_tasks = await session.execute(select(OnboardingTask))
        if not existing_tasks.scalars().first():
            for task_data in DEFAULT_TASKS:
                task = OnboardingTask(**task_data)
                session.add(task)
            print(f"✅ {len(DEFAULT_TASKS)} onboarding tasks created")
        else:
            print("ℹ️  Onboarding tasks already exist")

        await session.commit()

    # --- Seed Knowledge Base (Phase 2) ---
    print("\n📚 Seeding knowledge base...")
    async with async_session() as session:
        try:
            from app.services.knowledge_service import knowledge_service
            count = await knowledge_service.ingest_default_faqs(session)
            await session.commit()
            if count > 0:
                print(f"✅ {count} FAQ entries ingested into knowledge base")
            else:
                print("ℹ️  FAQ entries already exist in knowledge base")

            # Print vector store stats
            stats = await knowledge_service.get_vector_store_stats()
            print(f"📊 Vector store: {stats.get('document_count', 0)} documents indexed")
        except Exception as e:
            print(f"⚠️  Knowledge base seeding skipped: {e}")
            print("   (This is normal if ChromaDB dependencies aren't installed yet)")

    print("\n🌱 Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
