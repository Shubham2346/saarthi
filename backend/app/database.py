"""
Database engine, session, and initialization for async SQLModel + PostgreSQL.
Supports alembic migrations with create_all fallback.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Async engine for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),
    future=True,
    pool_size=20,
    max_overflow=10,
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency that yields an async database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all database tables on startup (fallback when alembic hasn't run)."""
    import app.models  # noqa: F401 — register models with SQLModel metadata

    # Try to run alembic migrations first; fall back to create_all
    try:
        from alembic.config import Config
        from alembic.command import upgrade as alembic_upgrade
        import os

        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
        alembic_upgrade(alembic_cfg, "head")
        print("Alembic migrations applied to head")
    except Exception as e:
        print(f"Alembic migration skipped ({e}), using create_all fallback")

        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    # Seed RBAC roles and permissions
    try:
        from app.services.rbac_service import (
            seed_default_roles, seed_permissions, seed_role_permissions,
        )
        from app.database import async_session

        async with async_session() as session:
            await seed_default_roles(session)
            await seed_permissions(session)
            await seed_role_permissions(session)
            await session.commit()
            print("RBAC roles and permissions seeded")
    except Exception as e:
        print(f"RBAC seeding skipped: {e}")


async def close_db():
    """Dispose of the database engine on shutdown."""
    await engine.dispose()
