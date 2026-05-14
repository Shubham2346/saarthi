# Saarthi — Smart Student Onboarding Assistant

## Overview

Saarthi is a modern, production-ready student onboarding platform with an AI-powered assistant, comprehensive task management, and document tracking. This application streamlines the college admissions and onboarding process.

### Key Features

✨ **Modern UI/UX**
- Clean, professional design with modern layouts
- Responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Professional color palette with gradients

🔐 **Authentication System**
- Email/Password registration and login
- Google OAuth integration
- Forgot password functionality
- Secure JWT-based sessions
- Protected routes

🎯 **Student Onboarding**
- Personalized task tracking with deadlines
- Progress tracking dashboard
- Document upload and management
- AI-powered chatbot assistance
- Knowledge base with FAQs

📊 **Dashboard**
- Real-time progress visualization
- Task statistics (completed, pending, overdue)
- Quick action buttons
- System status monitoring
- Personalized greeting

---

## Project Structure

```
saarthi/
├── frontend/               # Next.js React application
│   ├── app/               # App router pages
│   │   ├── login/         # Login page
│   │   ├── signup/        # Sign up page
│   │   ├── forgot-password/
│   │   ├── dashboard/     # Main dashboard
│   │   ├── chat/          # AI chat interface
│   │   └── tasks/         # Task management
│   ├── components/        # Reusable React components
│   │   ├── AppShell.js    # Main layout wrapper
│   │   └── Sidebar.js     # Navigation sidebar
│   ├── lib/               # Utilities and helpers
│   │   ├── api.js         # API client
│   │   ├── auth.js        # Auth context and hooks
│   │   └── protected-route.js  # Route protection
│   ├── app/globals.css    # Tailwind CSS setup
│   └── tailwind.config.js # Tailwind configuration
│
└── backend/               # FastAPI Python application
    ├── app/
    │   ├── main.py        # App entry point
    │   ├── config.py      # Settings
    │   ├── database.py    # DB connection
    │   ├── routers/       # API endpoints
    │   │   ├── auth.py    # Authentication routes
    │   │   ├── chat.py    # Chat/AI routes
    │   │   └── ...
    │   ├── services/      # Business logic
    │   │   └── auth_service.py
    │   ├── models/        # SQLModel definitions
    │   └── schemas/       # Pydantic schemas
    └── requirements.txt   # Python dependencies
```

---

## Frontend Setup

### Prerequisites

- Node.js 18+ and npm/yarn
- Modern web browser

### Installation

```bash
cd frontend
npm install
```

### Available Scripts

```bash
# Development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Environment Variables

Create `.env.local` in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Key Technologies

- **Next.js 16** - React framework with server-side rendering
- **React 19** - UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library
- **React Hook Form** - Form state management
- **Zod** - Schema validation
- **Framer Motion** - Animation library

---

## Backend Setup

### Prerequisites

- Python 3.10+
- pip or poetry

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables

Create `.env` in the backend directory:

```env
# App Config
APP_NAME=Saarthi
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/saarthi_db

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Frontend
FRONTEND_URL=http://localhost:3000

# Ollama (for AI)
OLLAMA_BASE_URL=http://localhost:11434
```

### Running the Backend

```bash
# Development server (http://localhost:8000)
uvicorn app.main:app --reload

# Access API docs
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Key Technologies

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL + Python type hints
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Python-Jose** - JWT authentication
- **Passlib** - Password hashing
- **LangChain** - LLM orchestration
- **ChromaDB** - Vector database

---

## Authentication Flow

### Email/Password Registration

1. User fills signup form with email, password, name
2. Backend validates input and checks for existing email
3. Password hashed using bcrypt
4. User record created in database
5. JWT token generated and returned
6. Frontend stores token and user data in localStorage
7. User redirected to dashboard

### Email/Password Login

1. User enters email and password
2. Backend verifies email exists and password matches
3. JWT token generated on successful match
4. Frontend stores token and user data
5. User redirected to dashboard

### Google OAuth

1. User clicks "Continue with Google"
2. Google sign-in window opens
3. User authenticates with Google
4. Frontend receives ID token from Google
5. Token sent to backend for verification
6. Backend verifies with Google's servers
7. User created or fetched from database
8. JWT token generated and returned
9. User logged in and redirected

### Protected Routes

- Login page redirects to dashboard if already logged in
- All protected pages require valid JWT token
- Invalid/expired tokens redirect to login
- User data automatically refreshed on app load

---

## API Endpoints

### Authentication

```
POST /api/v1/auth/register
  Body: { email, password, name }
  Response: { access_token, token_type, user }

POST /api/v1/auth/login
  Body: { email, password }
  Response: { access_token, token_type, user }

POST /api/v1/auth/google
  Body: { id_token }
  Response: { access_token, token_type, user }

POST /api/v1/auth/forgot-password
  Body: { email }
  Response: { message }

GET /api/v1/auth/me
  Headers: Authorization: Bearer {token}
  Response: { user_data }
```

### Tasks

```
GET /api/v1/tasks/me
  Get user's tasks

PATCH /api/v1/tasks/me/{taskId}
  Update task status

GET /api/v1/tasks/me/progress
  Get progress statistics
```

### Chat

```
POST /api/v1/chat/
  Body: { message, category }
  Send message to AI

POST /api/v1/chat/search
  Body: { query, category, n_results }
  Search knowledge base

GET /api/v1/chat/health
  Get system health status
```

---

## Database Schema

### Users Table

```sql
- id (UUID) - Primary key
- email (String) - Unique email
- full_name (String) - User's name
- hashed_password (String) - Bcrypt hash
- google_id (String) - Google OAuth ID
- avatar_url (String) - Profile picture
- role (Enum) - student/admin/mentor
- stage (Enum) - Onboarding stage
- created_at (DateTime)
- updated_at (DateTime)
```

### User Tasks Table

```sql
- id (UUID) - Primary key
- user_id (UUID) - Foreign key to users
- title (String) - Task name
- description (Text) - Details
- due_date (DateTime) - Deadline
- completed_at (DateTime) - Completion time
- status (Enum) - pending/completed/overdue
```

### Documents Table

```sql
- id (UUID) - Primary key
- user_id (UUID) - Foreign key
- file_name (String)
- file_size (Integer)
- mime_type (String)
- uploaded_at (DateTime)
```

---

## Frontend Features in Detail

### Authentication Pages

**Login Page (`/login`)**
- Email/password form
- Social login buttons (Google, GitHub, Apple, Facebook)
- Remember me option
- Forgot password link
- Sign up link
- Error handling and validation

**Sign Up Page (`/signup`)**
- Full name, email, password fields
- Password confirmation
- Terms agreement checkbox
- Social sign up options
- Error handling
- Success message with redirect

**Forgot Password Page (`/forgot-password`)**
- Email input field
- Reset link submission
- Success confirmation
- Back to login option

### Dashboard

**Main Dashboard (`/dashboard`)**
- Welcome greeting with time-based greeting
- Progress visualization
- Task statistics cards
- Quick action buttons
- System status indicator
- Getting started tips
- Responsive grid layout

**Responsive Design**
- Mobile-first approach
- Tablet optimization
- Desktop full layout
- Touch-friendly navigation
- Collapsible sidebar on mobile

### Navigation

**Sidebar Navigation**
- Responsive design (hidden on mobile)
- Active page indicator
- User profile section
- Quick logout button
- Admin-specific menu items

**Mobile Menu**
- Hamburger menu toggle
- Full-screen menu on mobile
- Same navigation items as desktop
- Close on link click

---

## Styling & Design System

### Color Palette

- **Primary**: Indigo (`#6366f1`)
- **Accent**: Green (`#22c55e`)
- **Danger**: Red (`#ef4444`)
- **Background**: White/Gray (`#ffffff`, `#f9fafb`)
- **Text**: Gray (`#1f2937`, `#6b7280`)

### Tailwind CSS Classes

Key component classes:
- `.btn`, `.btn-primary`, `.btn-secondary`
- `.input`, `.card`, `.badge`
- `.container`, `.prose`

### Animations

- Smooth fade-in effects
- Blob animations (background)
- Button hover states
- Loading spinners
- Transition effects

---

## Security Best Practices

✅ **Implemented**
- Passwords hashed with bcrypt
- JWT tokens with expiry
- CORS protection
- HTTP-only cookies ready
- Protected API routes
- Input validation with Zod
- Environment variable protection

🔒 **Recommendations**
- Use HTTPS in production
- Set secure JWT secret
- Implement rate limiting
- Add email verification
- Implement refresh tokens
- Use environment-specific configs
- Add request logging
- Enable security headers

---

## Error Handling

### Frontend
- API error alerts with user-friendly messages
- Form validation with field-level errors
- Network error recovery
- Automatic redirect on 401 (auth)
- Try-catch blocks for async operations

### Backend
- Comprehensive HTTP status codes
- Detailed error messages
- Validation error responses
- Exception handling middleware
- Logging of errors

---

## Performance Optimization

- **Code Splitting**: Dynamic imports for routes
- **Image Optimization**: Next.js Image component ready
- **CSS**: Tailwind purges unused styles
- **Caching**: API response caching with headers
- **Lazy Loading**: Components loaded on demand

---

## Testing

### Frontend (TODO)
```bash
npm run test
```

### Backend (TODO)
```bash
pytest tests/
```

---

## Deployment

### Frontend (Vercel)

```bash
# Connect GitHub repo to Vercel
# Set environment variables in Vercel dashboard
# Push to main branch for auto-deployment
```

### Backend (Railway/Render)

```bash
# Push to hosting provider
# Set environment variables
# Auto-deploy on push
```

---

## Troubleshooting

### Login Issues
- Check API URL in `.env.local`
- Verify backend is running
- Clear browser localStorage
- Check token expiry

### Database Connection
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Run migrations if needed
- Check user permissions

### CORS Errors
- Verify FRONTEND_URL in backend
- Check API_BASE in frontend
- Ensure credentials are allowed

---

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

---

## License

MIT License - see LICENSE file

---

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@saarthi.app

---

## Roadmap

- [x] Modern authentication system
- [x] Responsive dashboard
- [ ] Real-time notifications
- [ ] Video integration
- [ ] Payment gateway
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Advanced AI features

---

**Last Updated**: May 2026

Built with ❤️ for students
