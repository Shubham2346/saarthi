# Quick Start Guide - Saarthi Development

## 🚀 Get Started in 5 Minutes

### Prerequisites Check

```bash
# Check Node.js version (need 18+)
node --version

# Check Python version (need 3.10+)
python --version

# Check PostgreSQL (optional, uses SQLite in dev)
psql --version
```

---

## 📦 Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1' > .env.local

# Start development server
npm run dev
```

**Access**: http://localhost:3000

### Available Pages

- `/login` - Login page (email/password + social)
- `/signup` - Sign up page
- `/forgot-password` - Password reset
- `/dashboard` - Main dashboard (after login)

---

## 🐍 Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
APP_NAME=Saarthi
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./saarthi.db
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your-google-client-id
FRONTEND_URL=http://localhost:3000
OLLAMA_BASE_URL=http://localhost:11434
EOF

# Start development server
uvicorn app.main:app --reload
```

**Access**:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Test the Application

### 1. Test Sign Up (Email/Password)

**Frontend**: Go to http://localhost:3000/signup

```
Name: John Doe
Email: john@example.com
Password: Password123!
Confirm: Password123!
```

Expected: Account created, redirect to dashboard

### 2. Test Login

**Frontend**: Go to http://localhost:3000/login

```
Email: john@example.com
Password: Password123!
```

Expected: Login successful, redirect to dashboard

### 3. Test Dashboard

After login, you should see:
- Progress card (0%)
- 4 metrics cards
- Quick action buttons
- System status

### 4. Test API Directly (Swagger)

Visit http://localhost:8000/docs

**Try Register**:
1. Click "Try it out" on POST /auth/register
2. Fill in request:
   ```json
   {
     "email": "test@example.com",
     "password": "Test123!",
     "name": "Test User"
   }
   ```
3. Click Execute
4. Copy the `access_token` from response

**Test Protected Endpoint**:
1. Click on GET /auth/me
2. Click "Authorize" button (top right)
3. Paste: `Bearer {access_token}`
4. Try it out - should return user data

---

## 📝 Common Tasks

### Modify API URL

**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Add a New Route

**Backend** (`app/routers/example.py`):
```python
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/hello")
async def hello():
    return {"message": "Hello World"}
```

Then register in `app/main.py`:
```python
from app.routers import example
app.include_router(example.router)
```

### Add a New Frontend Page

**Create** `app/newpage/page.js`:
```javascript
'use client'

export default function NewPage() {
  return <div>New Page Content</div>
}
```

Access at: http://localhost:3000/newpage

### Run Backend Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

---

## 🎨 Styling Guide

### Using Tailwind CSS

```jsx
// Component with Tailwind
<div className="bg-indigo-600 text-white p-4 rounded-lg hover:bg-indigo-700">
  Button
</div>
```

### Available Utilities

```
Colors: bg-indigo-600, text-gray-700, border-gray-200
Spacing: p-4, m-2, gap-3
Typography: font-bold, text-lg, uppercase
Flexbox: flex, items-center, justify-between
Grid: grid, grid-cols-4, gap-6
Responsive: md:, lg:, xl:
```

### Custom Theme Colors

Edit `tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      brand: {
        50: '#f8f9ff',
        600: '#6366f1',
        700: '#4f46e5',
      }
    }
  }
}
```

---

## 🐛 Debugging

### Frontend Debug Mode

Check browser console:
```javascript
// In page.js
console.log('User:', user)
console.log('Error:', error)
```

Enable React DevTools extension in browser.

### Backend Debug Mode

```python
# In Python file
import logging
logging.debug("Debug message")

# Or
print("Debug info:", variable)
```

Check terminal output where server is running.

### API Response Debugging

Use browser DevTools Network tab:
1. Open DevTools (F12)
2. Go to Network tab
3. Perform action
4. Click on request
5. View Response

---

## 📚 Project Structure Summary

```
Frontend: React + Next.js + Tailwind
├── Pages (app/)
├── Components (components/)
├── Utilities (lib/)
└── Styles (globals.css)

Backend: FastAPI + SQLModel
├── Routes (routers/)
├── Models (models/)
├── Services (services/)
└── Database (database.py)
```

---

## 🚨 Troubleshooting

### Port Already in Use

**Frontend**:
```bash
# Kill process on port 3000
# Windows: netstat -ano | findstr :3000
# macOS/Linux: lsof -i :3000 | grep LISTEN
# Kill: kill -9 <PID>

# Or use different port
npm run dev -- -p 3001
```

**Backend**:
```bash
# Kill process on port 8000
# macOS/Linux: lsof -i :8000 | grep LISTEN
# Windows: netstat -ano | findstr :8000

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### CORS Error

Make sure `FRONTEND_URL` in backend `.env` matches your frontend URL.

### Login Fails

1. Check API URL in `.env.local`
2. Verify backend is running
3. Check email/password format
4. Look at backend logs for error

### Database Error

Clear database and restart:
```bash
# Backend
rm saarthi.db  # SQLite file
```

Restart backend to recreate tables.

---

## 📖 Useful Links

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Docs](https://react.dev/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)

---

## 💡 Tips & Tricks

### Clear Cache & Cookies

```javascript
// Frontend browser console
localStorage.clear()
sessionStorage.clear()
// Then reload page
```

### Hot Reload

Both frontend and backend support hot reload:
- Frontend: Changes reflect instantly
- Backend: Changes reflected on save (uvicorn --reload)

### Quick API Test

```bash
# Test login endpoint
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### View All Routes

**Frontend**: Check `components/Sidebar.js` for navigation items

**Backend**: Visit http://localhost:8000/docs

---

## 🎯 Next Steps

1. ✅ Setup frontend and backend
2. ✅ Test sign up and login
3. ✅ Explore dashboard
4. 📝 Read `FRONTEND_REDESIGN.md` for detailed docs
5. 🔧 Start building features

---

**Happy coding! 🚀**
