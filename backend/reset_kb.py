import asyncio
from sqlmodel import delete
from app.database import async_session, init_db
from app.models.knowledge import KnowledgeEntry
from app.seed import seed_database

async def reset_kb():
    await init_db()
    async with async_session() as session:
        await session.execute(delete(KnowledgeEntry))
        await session.commit()
    print("Deleted all knowledge_entries from Postgres.")
    
if __name__ == "__main__":
    asyncio.run(reset_kb())
