import asyncio
from sqlalchemy import text
from app.database import engine

async def migrate():
    print("Running migrations...")
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN department VARCHAR(100)"))
        except Exception as e:
            print(f"department already exists? {e}")
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN program VARCHAR(100)"))
        except Exception:
            pass
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN batch VARCHAR(20)"))
        except Exception:
            pass
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN mentor_id UUID REFERENCES users(id)"))
        except Exception:
            pass
    print("Migrations complete.")

if __name__ == "__main__":
    asyncio.run(migrate())
