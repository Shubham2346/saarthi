"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- App ---
    APP_NAME: str = "Saarthi"
    APP_ENV: str = "development"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"

    # --- Server ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/saarthi"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/saarthi"

    # --- JWT ---
    JWT_SECRET_KEY: str = "change-this-in-production-use-a-strong-random-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # --- File Uploads ---
    UPLOAD_DIR: str = "./storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: list = ["pdf", "jpg", "jpeg", "png", "docx", "doc"]

    # --- Ollama (Phase 2+) ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"
    OLLAMA_VISION_MODEL: str = "llama3.2-vision"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000
    LLM_TIMEOUT: int = 60

    # --- Vector DB (Phase 2+) ---
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    VECTOR_DB_TYPE: str = "chromadb"
    VECTOR_DB_PATH: str = "./storage/vector_db"
    QDRANT_URL: Optional[str] = None
    EMBEDDING_MODEL: str = "ollama"
    EMBEDDING_MODEL_NAME: str = "nomic-embed-text"
    VECTOR_CHUNK_SIZE: int = 1000
    VECTOR_CHUNK_OVERLAP: int = 200

    # --- OCR ---
    TESSERACT_PATH: Optional[str] = None
    ENABLE_OCR: bool = True
    OCR_LANGUAGE: str = "eng+hin"

    # --- S3 ---
    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = "saarthi-uploads"
    AWS_S3_REGION: str = "us-east-1"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600

    # --- Email (password reset, notifications) ---
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@localhost"
    SMTP_USE_TLS: bool = True
    PASSWORD_RESET_TOKEN_HOURS: int = 24

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    LOG_FILE: str = "app.log"

    # --- Sentry ---
    SENTRY_DSN: Optional[str] = None

    # --- Feature Flags ---
    ENABLE_ADMIN_DASHBOARD: bool = True
    ENABLE_ESCALATION_AGENT: bool = True
    ENABLE_DOCUMENT_VERIFICATION: bool = True
    ENABLE_RAG_SEARCH: bool = True
    ENABLE_VECTOR_DB: bool = True

    # --- LangGraph ---
    LANGGRAPH_DEBUG: bool = False
    AGENT_TIMEOUT: int = 30
    MAX_AGENT_ITERATIONS: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton to avoid re-reading .env on every request."""
    return Settings()
