# Saarthi — Smart Student Onboarding Agent

> An AI-powered, multi-agent student onboarding system for engineering colleges.

## 🏗️ Project Structure

```
Saarthi/
├── backend/          # FastAPI + SQLModel + PostgreSQL
│   ├── app/
│   │   ├── main.py           # App entry point
│   │   ├── config.py         # Environment config
│   │   ├── database.py       # Async DB engine
│   │   ├── seed.py           # Database seeder
│   │   ├── models/           # SQLModel ORM models
│   │   ├── schemas/          # Pydantic request/response DTOs
│   │   ├── routers/          # API route handlers
│   │   ├── services/         # Business logic layer
│   │   └── middleware/       # JWT auth middleware
│   ├── requirements.txt
│   └── .env.example
└── frontend/         # Next.js (coming in next phase)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Node.js 18+ (for frontend, later)

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env with your database credentials and Google OAuth keys

# 5. Create PostgreSQL database
# CREATE DATABASE saarthi;

# 6. Seed the database with default tasks
python -m app.seed

# 7. Run the development server
uvicorn app.main:app --reload --port 8000
```

### API Documentation
Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/google` | Login with Google OAuth token |
| GET | `/api/v1/auth/me` | Get current user profile |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/` | List all users (admin) |
| GET | `/api/v1/users/{id}` | Get user profile |
| PATCH | `/api/v1/users/me` | Update own profile |
| PATCH | `/api/v1/users/{id}` | Update any user (admin) |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks/templates` | Create task template (admin) |
| GET | `/api/v1/tasks/templates` | List all task templates |
| GET | `/api/v1/tasks/my-tasks` | Get student's assigned tasks |
| GET | `/api/v1/tasks/my-progress` | Get onboarding progress |
| PATCH | `/api/v1/tasks/my-tasks/{id}` | Update task status |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/documents/upload` | Upload a document |
| GET | `/api/v1/documents/my-documents` | List my documents |
| GET | `/api/v1/documents/pending` | List pending docs (admin) |
| PATCH | `/api/v1/documents/{id}/verify` | Verify/reject doc (admin) |

### Support Tickets
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tickets/` | Create support ticket |
| GET | `/api/v1/tickets/my-tickets` | List my tickets |
| GET | `/api/v1/tickets/` | List all tickets (admin) |
| PATCH | `/api/v1/tickets/{id}` | Update ticket (admin) |

## 🗺️ Roadmap

- [x] **Phase 1:** Foundation & Data Modeling
- [ ] **Phase 2:** Knowledge Base & RAG (ChromaDB + Ollama)
- [ ] **Phase 3:** Multi-Agent System (LangGraph)
- [ ] **Phase 4:** Document Verification Agent (Tesseract + Vision LLM)
- [ ] **Phase 5:** Polish, Analytics, and Deployment

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + SQLModel |
| Database | PostgreSQL |
| Auth | Google OAuth + JWT |
| Frontend | Next.js + TailwindCSS |
| AI Agents | LangGraph + Ollama |
| Vector DB | ChromaDB |
| OCR | Tesseract |
