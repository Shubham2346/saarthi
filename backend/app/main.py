"""
Saarthi — Smart Student Onboarding Agent
FastAPI Application Entry Point

This is the main application file that configures CORS, registers routers,
and manages the application lifecycle (DB init, shutdown).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db, close_db
from app.routers import auth, users, tasks, documents, tickets, chat, knowledge

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle — initializes DB on startup, cleans up on shutdown."""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} Backend...")
    await init_db()
    print("✅ Database tables created/verified")
    yield
    # Shutdown
    print(f"🛑 Shutting down {settings.APP_NAME} Backend...")
    await close_db()


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

# --- CORS Configuration ---
# Allow the frontend origin and common development ports
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

# --- Register Routers ---
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")


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
