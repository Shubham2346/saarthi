"""
Saarthi — Smart Student Onboarding Agent
FastAPI Application Entry Point

This is the main application file that configures CORS, registers routers,
and manages the application lifecycle (DB init, shutdown).
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db, close_db
from app.routers import auth, users, tasks, documents, tickets, chat, knowledge, admission, admin, roles, mentor, coordinator, sysadmin

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle — initializes DB on startup, cleans up on shutdown."""
    print(f"Starting {settings.APP_NAME} Backend...")
    try:
        await init_db()
        print("Database tables created/verified")

        # Auto-seed knowledge base if empty
        try:
            from app.database import async_session
            from app.services.knowledge_service import knowledge_service

            async with async_session() as session:
                new_count = await knowledge_service.ingest_default_faqs(session)
                await session.commit()
                if new_count > 0:
                    print(f"Knowledge base seeded with {new_count} new entries")
                else:
                    print("Knowledge base already seeded — skipping")
        except Exception as e:
            print(f"Knowledge base seeding skipped: {e}")
    except Exception as e:
        print(f"Database initialization skipped: {e}")
        print("(Server will still start — DB-dependent endpoints will fail)")
    yield
    print(f"Shutting down {settings.APP_NAME} Backend...")
    try:
        await close_db()
    except Exception:
        pass


app = FastAPI(
    title=f"{settings.APP_NAME} API",
    description=(
        "Smart Student Onboarding Agent — Backend API for managing student onboarding, "
        "document verification, task tracking, and AI-powered assistance."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Custom Middleware (order matters: logging outer, rate limit inner) ---
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.ratelimit import RateLimitMiddleware

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=200, window_seconds=60)


# --- Register Routers ---
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(admission.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(mentor.router, prefix="/api/v1")
app.include_router(coordinator.router, prefix="/api/v1")
app.include_router(sysadmin.router, prefix="/api/v1")


# --- Health Check ---
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "app": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Detailed health check with database, Ollama, and vector store connectivity."""
    from app.database import engine
    from sqlalchemy import text
    from app.services.ollama_service import ollama_service
    from app.services.vector_store import vector_store

    # Database check
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    # Ollama check
    ollama_status = await ollama_service.check_health()

    # Vector store check
    vector_status = vector_store.get_collection_stats()

    return {
        "app": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0",
        "database": db_status,
        "ollama": ollama_status,
        "vector_store": vector_status,
    }
