# Installation & Setup Instructions

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Frontend Setup](#frontend-setup)
3. [Backend Setup](#backend-setup)
4. [Database Configuration](#database-configuration)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- Node.js 18.0 or higher
- Python 3.10 or higher
- PostgreSQL 12+ (optional, SQLite works for development)
- 2GB RAM minimum
- 500MB disk space

### Recommended Setup
- Node.js 18+ or 20 LTS
- Python 3.11 LTS
- PostgreSQL 15
- 4GB RAM
- Git for version control

### Supported Operating Systems
- ✅ macOS (Intel & Apple Silicon)
- ✅ Ubuntu/Debian Linux
- ✅ Windows 10/11 (WSL2 recommended)
- ✅ CentOS/RHEL

---

## Frontend Setup

### Step 1: Install Node.js & npm

**macOS (using Homebrew)**:
```bash
brew install node
```

**Ubuntu/Debian**:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows**:
- Download from https://nodejs.org/
- Run installer and follow prompts

**Verify Installation**:
```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourname/saarthi.git
cd saarthi/frontend
```

### Step 3: Install Dependencies

```bash
# Using npm
npm install

# Or using yarn
yarn install
```

This installs:
- Next.js framework
- React and React DOM
- Tailwind CSS
- Lucide icons
- Form and validation libraries
- Authentication libraries

### Step 4: Configure Environment

Create `.env.local` file:

```bash
cat > .env.local << 'EOF'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Enable debug mode (optional)
# NEXT_PUBLIC_DEBUG=true
EOF
```

### Step 5: Start Development Server

```bash
npm run dev
```

Expected output:
```
▲ Next.js 16.2.6
- Local:        http://localhost:3000
- Environments: .env.local
```

**Access Frontend**: http://localhost:3000

---

## Backend Setup

### Step 1: Install Python

**macOS**:
```bash
# Using Homebrew
brew install python@3.11
```

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev
```

**Windows**:
- Download Python 3.11 from https://www.python.org/downloads/
- ⚠️ Important: Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and run `python --version`

### Step 2: Navigate to Backend

```bash
cd backend
```

### Step 3: Create Virtual Environment

**macOS/Linux**:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt)**:
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

After activation, your prompt should show `(venv)` prefix.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Installs:
- FastAPI framework
- Uvicorn ASGI server
- SQLModel ORM
- Pydantic validation
- Authentication libraries
- Database drivers
- And more...

### Step 5: Configure Environment

Create `.env` file in backend directory:

```bash
# macOS/Linux
cat > .env << 'EOF'
# Application
APP_NAME=Saarthi
APP_ENV=development
DEBUG=true

# Database (choose one)
# SQLite (development)
DATABASE_URL=sqlite:///./saarthi.db

# PostgreSQL (production)
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/saarthi_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com

# Frontend
FRONTEND_URL=http://localhost:3000

# Ollama (for AI features)
OLLAMA_BASE_URL=http://localhost:11434
EOF
```

**Windows (Command Prompt)**:
```cmd
(Use a text editor to create .env file with same content)
```

### Step 6: Initialize Database

```bash
# Database tables are created automatically on first run
# If needed, you can seed data:
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

### Step 7: Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Access Backend**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

## Database Configuration

### Option 1: SQLite (Development)

Easiest option for local development.

**Configuration** (.env):
```env
DATABASE_URL=sqlite:///./saarthi.db
```

**Automatic Setup**: Tables created on first run.

**Pros**: No installation, file-based, easy backup
**Cons**: Not suitable for production, limited concurrency

### Option 2: PostgreSQL (Production)

More robust for production deployments.

**Installation**:

**macOS**:
```bash
brew install postgresql
brew services start postgresql
createdb saarthi_db
createuser saarthi_user -P  # Enter password when prompted
```

**Ubuntu/Debian**:
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb saarthi_db
sudo -u postgres createuser saarthi_user -P
```

**Windows**:
- Download PostgreSQL installer
- Install and note the password
- Open pgAdmin to verify

**Create Database**:
```bash
psql -U postgres
CREATE DATABASE saarthi_db;
CREATE USER saarthi_user WITH PASSWORD 'secure_password';
ALTER ROLE saarthi_user SET client_encoding TO 'utf8';
ALTER ROLE saarthi_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE saarthi_db TO saarthi_user;
\q
```

**Configuration** (.env):
```env
DATABASE_URL=postgresql+asyncpg://saarthi_user:secure_password@localhost:5432/saarthi_db
```

**Verify Connection**:
```bash
psql -U saarthi_user -d saarthi_db
```

---

## Environment Variables

### Frontend (.env.local)

```env
# API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional: Google Analytics, Sentry, etc.
# NEXT_PUBLIC_GOOGLE_ID=
# NEXT_PUBLIC_SENTRY_DSN=
```

### Backend (.env)

```env
# === Application Settings ===
APP_NAME=Saarthi
APP_ENV=development              # development, staging, production
DEBUG=true                        # Set to false in production

# === Database ===
DATABASE_URL=sqlite:///./saarthi.db

# === JWT & Security ===
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# === Google OAuth ===
GOOGLE_CLIENT_ID=your-google-id.apps.googleusercontent.com

# === CORS ===
FRONTEND_URL=http://localhost:3000

# === AI/LLM ===
OLLAMA_BASE_URL=http://localhost:11434
```

### Production Environment Variables

```env
# === Security ===
APP_ENV=production
DEBUG=false
JWT_SECRET_KEY=<generate-strong-random-key>

# === Database ===
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/saarthi

# === Frontend ===
FRONTEND_URL=https://app.saarthi.com

# === Email (for forgot password) ===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=noreply@saarthi.com
SMTP_PASSWORD=<app-password>

# === Google OAuth ===
GOOGLE_CLIENT_ID=prod-google-id.apps.googleusercontent.com

# === Other ===
SENTRY_DSN=<sentry-url>
LOG_LEVEL=INFO
```

---

## Running the Application

### Complete Development Setup

**Terminal 1 - Frontend**:
```bash
cd frontend
npm run dev
```

**Terminal 2 - Backend**:
```bash
cd backend
source venv/bin/activate  # Or: venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 3 (Optional) - Database (if using PostgreSQL)**:
```bash
# If database service isn't running
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web application |
| Backend API | http://localhost:8000 | API endpoints |
| Swagger Docs | http://localhost:8000/docs | Interactive API docs |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
| Database (PostgreSQL) | localhost:5432 | Database server |

---

## Verification

### Verify Frontend

1. Open http://localhost:3000 in browser
2. Should see login page with:
   - Email/password form
   - Social login buttons
   - Sign up link
   - Forgot password link

3. Check browser console (F12) for errors
4. Should show no red errors in console

### Verify Backend

1. Open http://localhost:8000/docs in browser
2. Should see Swagger UI with all endpoints
3. Try executing a test request:
   - Expand "POST /auth/register"
   - Click "Try it out"
   - Fill in test data
   - Click "Execute"
   - Should return 200 status with token

### Verify Database Connection

**SQLite**:
```bash
ls -la saarthi.db  # Should exist and have size > 0
```

**PostgreSQL**:
```bash
psql -U saarthi_user -d saarthi_db -c "\dt"
# Should show list of tables
```

### Full Integration Test

1. Open http://localhost:3000/signup
2. Fill in form:
   - Name: Test User
   - Email: test@example.com
   - Password: Test123!
3. Click "Create Account"
4. Should redirect to dashboard
5. Should see welcome message and metrics

---

## Troubleshooting

### Frontend Issues

**Port 3000 already in use**:
```bash
# Kill process
# macOS/Linux:
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**npm install errors**:
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Blank page or 404**:
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Check backend is running
- Check browser console for errors
- Try clearing cache: Ctrl+Shift+Delete

### Backend Issues

**Port 8000 already in use**:
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Module not found**:
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Database connection error**:
- SQLite: Check write permissions on directory
- PostgreSQL: Verify connection string in .env
- Verify database server is running

**Python version mismatch**:
```bash
# Check version
python --version  # Should be 3.10+

# Use specific Python version
python3.11 -m venv venv
```

### Authentication Issues

**Login always fails**:
1. Check backend is running (`http://localhost:8000/docs` accessible)
2. Check `FRONTEND_URL` in backend `.env` matches your frontend
3. Check browser localStorage isn't full
4. Check backend logs for error messages

**CORS errors**:
- Backend `FRONTEND_URL` must match frontend origin
- If using different port, update in `.env`

**Token expired immediately**:
- Check `JWT_SECRET_KEY` is set in `.env`
- Check system time is correct (JWT validates timestamp)
- Increase `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` for debugging

### Database Issues

**SQLite file locked**:
```bash
# Restart backend, it should auto-recover
# If not, delete and recreate:
rm saarthi.db
# Restart backend
```

**PostgreSQL connection refused**:
```bash
# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Verify it's running
psql -U postgres -c "SELECT 1"
```

### Performance Issues

**Slow frontend**:
- Check Network tab in DevTools
- Verify API isn't slow
- Clear browser cache
- Rebuild: `npm run build`

**Slow backend**:
- Check backend logs for slow queries
- Monitor CPU/Memory usage
- Consider using PostgreSQL instead of SQLite

---

## Next Steps After Installation

1. ✅ Verify both frontend and backend are running
2. ✅ Test signup and login flow
3. ✅ Explore the dashboard
4. 📖 Read `FRONTEND_REDESIGN.md` for detailed documentation
5. 🔧 Start building features or customizing
6. 🚀 Plan deployment strategy

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review logs in terminals where services run
3. Check browser console (F12) for client-side errors
4. Check network requests in DevTools Network tab
5. Search GitHub issues
6. Create a new issue with:
   - Error message (full stack trace)
   - Steps to reproduce
   - System information (OS, Node/Python versions)
   - Screenshots if helpful

---

## Quick Reference

### Start Development
```bash
# Terminal 1: Frontend
cd frontend && npm run dev

# Terminal 2: Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload
```

### Build for Production
```bash
# Frontend
cd frontend && npm run build

# Backend
# Use production-grade ASGI server like Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Database Backup
```bash
# PostgreSQL
pg_dump -U saarthi_user saarthi_db > backup.sql

# Restore
psql -U saarthi_user saarthi_db < backup.sql
```

---

**Installation Complete!** 🎉

Your Saarthi application is now ready for development. Happy coding!
