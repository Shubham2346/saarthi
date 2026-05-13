# Saarthi Backend

Saarthi is a Smart Student Onboarding Agent backend API for managing student onboarding, document verification, task tracking, and AI-powered assistance.

This is a robust asynchronous Python backend built with FastAPI, integrating state-of-the-art AI tooling for document parsing, intelligent conversational agents, and Retrieval-Augmented Generation (RAG).

## 🚀 Tech Stack

### Core Framework
- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance asynchronous web framework for building the API.
- **Uvicorn**: Lightning-fast ASGI server.
- **Python**: 3.12+

### Database & ORM
- **PostgreSQL**: Primary relational database.
- **[SQLModel](https://sqlmodel.tiangolo.com/) / SQLAlchemy**: Modern Python ORM for database interactions.
- **asyncpg**: Fast asynchronous PostgreSQL database client.
- **Alembic**: Database migration tool.

### AI & Agents (RAG & NLP)
- **[LangChain](https://python.langchain.com/) / LangGraph**: Framework for developing applications powered by language models and creating complex multi-agent workflows.
- **[ChromaDB](https://www.trychroma.com/)**: Open-source embedding database for managing vector storage for RAG implementations.
- **[Ollama](https://ollama.com/)**: Local LLM execution engine running models like `gemma4:e2b` for chat and reasoning, and `llama3.2-vision` for visual tasks.
- **Tiktoken**: Tokenizer integration.

### Document Processing & OCR
- **Tesseract OCR (`pytesseract`)**: Optical Character Recognition engine to extract text from images/documents.
- **Pillow**: Python Imaging Library for handling images.

### Security & Authentication
- **JWT (JSON Web Tokens)**: Secure token-based authentication using `python-jose`.
- **Passlib (`bcrypt`)**: Secure password hashing.
- **Google OAuth**: Integration for external authentication.

### Utilities
- **Pydantic**: Data validation and settings management (`pydantic-settings`).
- **HTTPX**: Modern async HTTP client.
- **Aiofiles**: Asynchronous file handling.

## 📂 Project Structure

- `app/`
  - `agents/`: LangGraph agents and conversational logic.
  - `routers/`: FastAPI endpoint routes (`auth`, `users`, `tasks`, `documents`, `tickets`, `chat`, `knowledge`).
  - `models/`: SQLModel database models.
  - `schemas/`: Pydantic schemas for request/response validation.
  - `services/`: Core business logic (Ollama integration, Vector Store ops, OCR, etc.).
  - `middleware/`: Custom FastAPI middleware.
  - `config.py`: Application configuration via Pydantic settings.
  - `database.py`: Database connection setup and session management.
  - `main.py`: Application entry point.
- `alembic/`: Database migration scripts (if initialized).
- `chroma_data/`: Local persistent storage for ChromaDB.
- `.env`: Environment variables configuration.
- `requirements.txt`: Python package dependencies.

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.12+
- PostgreSQL
- [Ollama](https://ollama.com/) installed locally (if running AI features)
- Tesseract OCR installed on your system

### 1. Clone & Environment Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `backend` directory based on `.env.example`:

```env
APP_NAME="Saarthi"
APP_ENV="development"
FRONTEND_URL="http://localhost:3000"

DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/saarthi"
DATABASE_URL_SYNC="postgresql://postgres:postgres@localhost:5432/saarthi"

JWT_SECRET_KEY="your-secret-key"
JWT_ALGORITHM="HS256"

# Ollama & Chroma Config
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="gemma4:e2b"
OLLAMA_VISION_MODEL="llama3.2-vision"
CHROMA_PERSIST_DIR="./chroma_data"
```

### 3. Running the Server

Run the development server using `uvicorn`:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000
Interactive API Documentation (Swagger UI) will be at: http://localhost:8000/docs
