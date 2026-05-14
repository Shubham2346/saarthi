# QUICK START - GET SYSTEM RUNNING IN 15 MINUTES

**For Developers**: Get the system running locally on your machine.  
**For Admins**: Deploy to your server.

---

## 🟢 OPTION 1: LOCAL DEVELOPMENT (Docker Compose)

**Time Required:** 10 minutes  
**Requirements:** Docker installed

### Step 1: Navigate to Docker Directory

```bash
cd backend/deployment/docker
```

### Step 2: Create Environment File

Create `.env` in this directory:

```env
# Database
DATABASE_URL=sqlite:///./saarthi.db
DB_PASSWORD=your_secure_password

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this

# Frontend/Backend URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

# Ollama
OLLAMA_BASE_URL=http://ollama:11434

# Redis
REDIS_URL=redis://redis:6379

# Environment
APP_ENV=development
DEBUG=true

# Vector Database
VECTOR_DB_TYPE=chromadb
```

### Step 3: Start All Services

```bash
docker-compose up -d
```

This starts:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Ollama**: http://localhost:11434
- **Qdrant** (optional): http://localhost:6333

### Step 4: Wait for Services (2-3 minutes)

```bash
# Check status
docker-compose ps

# Wait for "ollama pull" to complete (first time only)
docker-compose logs ollama
```

Once all services show **Up**, proceed to step 5.

### Step 5: Access the System

**Frontend (Student Interface):**
```
http://localhost:3000
```

**Backend API Documentation:**
```
http://localhost:8000/docs
```

**Admin Dashboard:**
```
http://localhost:3000/admin
```

### Step 6: Create Test Account

```bash
# Access the API docs at http://localhost:8000/docs
# Find POST /api/v1/auth/signup
# Click "Try it out"
# Enter:
{
  "name": "Test Student",
  "email": "test@example.com",
  "password": "Test123!",
  "student_id": "TEST001"
}
# Click Execute
```

**Test Credentials:**
- Email: `test@example.com`
- Password: `Test123!`

### Step 7: Test Chat Interface

1. Login with test credentials
2. Click "Chat" in sidebar
3. Try these questions:

```
"What's my task?"
"What are hostel timings?"
"I need to upload my documents"
"Help! Nothing is working"
```

---

## 🟡 OPTION 2: STAGING DEPLOYMENT (Cloud Server)

**Time Required:** 45 minutes  
**Requirements:** Cloud server (Ubuntu 22.04), Docker installed

### Step 1: Server Preparation

```bash
# SSH into your server
ssh ubuntu@your-server-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version && docker-compose --version
```

### Step 2: Clone Repository

```bash
cd /opt
sudo git clone https://github.com/your-org/saarthi.git
sudo chown -R ubuntu:ubuntu saarthi
cd saarthi
```

### Step 3: Configure Environment

```bash
cd backend/deployment/docker

# Create production .env
cat > .env << 'EOF'
APP_ENV=staging
DEBUG=false
DATABASE_URL=postgresql+asyncpg://saarthi_user:$(openssl rand -base64 32)@postgres:5432/saarthi_db
JWT_SECRET_KEY=$(openssl rand -base64 32)
FRONTEND_URL=https://app.yourdomain.com
BACKEND_URL=https://app.yourdomain.com/api
OLLAMA_BASE_URL=http://ollama:11434
REDIS_URL=redis://redis:6379
VECTOR_DB_TYPE=qdrant
EOF

# Verify .env created
cat .env
```

### Step 4: Start Services

```bash
docker-compose up -d

# Wait for Ollama models to download (5-10 minutes)
docker-compose logs -f ollama
```

### Step 5: Configure Reverse Proxy (Nginx)

```bash
# Copy nginx config
sudo cp ../nginx/nginx.conf /etc/nginx/sites-available/saarthi

# Edit domain in nginx config
sudo sed -i 's/app.example.com/app.yourdomain.com/g' /etc/nginx/sites-available/saarthi

# Enable site
sudo ln -s /etc/nginx/sites-available/saarthi /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t && sudo systemctl reload nginx
```

### Step 6: SSL Certificate

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --nginx -d app.yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer && sudo systemctl start certbot.timer
```

### Step 7: Access System

```
https://app.yourdomain.com
```

---

## 🔴 OPTION 3: PRODUCTION DEPLOYMENT (Kubernetes)

**Time Required:** 2 hours  
**Requirements:** Kubernetes cluster, kubectl configured

### Step 1: Prepare Cluster

```bash
# Create namespace
kubectl create namespace saarthi

# Create secrets
kubectl create secret generic saarthi-secrets \
  --from-literal=jwt-secret-key=$(openssl rand -base64 32) \
  --from-literal=db-password=$(openssl rand -base64 32) \
  -n saarthi

# Verify
kubectl get secrets -n saarthi
```

### Step 2: Create PersistentVolumes

If using local storage:

```bash
# Create directories for persistent data
sudo mkdir -p /data/saarthi/{postgres,uploads,vector_db}
sudo chmod -R 755 /data/saarthi
```

### Step 3: Deploy Application

```bash
# Navigate to K8s manifests
cd backend/deployment/kubernetes

# Apply manifests
kubectl apply -f k8s-manifest.yaml

# Monitor deployment
kubectl get pods -n saarthi -w

# Check services
kubectl get services -n saarthi
```

### Step 4: Expose Application

```bash
# Option A: NodePort (for testing)
# Already exposed by manifest on port 30000

# Option B: LoadBalancer
kubectl patch svc frontend-service -n saarthi -p '{"spec": {"type": "LoadBalancer"}}'

# Get external IP
kubectl get svc -n saarthi
```

### Step 5: Setup Ingress

```bash
# Install Ingress Controller (if not present)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace

# Create ingress
cat > ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: saarthi-ingress
  namespace: saarthi
spec:
  ingressClassName: nginx
  rules:
  - host: app.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
EOF

kubectl apply -f ingress.yaml
```

### Step 6: Access Application

```
https://app.yourdomain.com
```

---

## 🧪 TESTING AFTER DEPLOYMENT

### Test 1: Frontend Access

```bash
# Open in browser
http://localhost:3000  # Local
https://app.yourdomain.com  # Staging/Production

# You should see:
✓ Login page loads
✓ Signup form renders
✓ Mobile responsive
```

### Test 2: Backend API

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
{"status": "healthy"}
```

### Test 3: Create User

```bash
# Via API
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "email": "test@example.com",
    "password": "Test123!",
    "student_id": "TEST001"
  }'

# Or via web interface at http://localhost:3000/signup
```

### Test 4: Chat Interface

```bash
# Login
# Navigate to Chat
# Send: "What's my task?"
# Expected: System responds with task list
```

### Test 5: Document Upload

```bash
# Login
# Navigate to Documents
# Upload a PDF or image
# Expected: 
# ✓ File uploaded
# ✓ OCR processing shows status
# ✓ Extracted text displayed (if clear)
```

### Test 6: Admin Dashboard

```bash
# Navigate to: http://localhost:3000/admin
# Expected:
# ✓ Dashboard loads
# ✓ Analytics showing
# ✓ User management visible
```

---

## 🔧 COMMON TROUBLESHOOTING

### Problem: Ollama Models Not Downloaded

```bash
# Check Ollama logs
docker-compose logs ollama

# Manually pull models
docker exec docker_ollama_1 ollama pull llama2
docker exec docker_ollama_1 ollama pull llava

# Wait 5-10 minutes for download to complete
```

### Problem: Database Connection Error

```bash
# Check PostgreSQL
docker exec docker_postgres_1 psql -U saarthi_user -d saarthi_db -c "SELECT 1"

# If error, check env vars
docker-compose config | grep DATABASE_URL

# Reset database
docker-compose down -v  # Warning: deletes data!
docker-compose up -d
```

### Problem: Frontend Not Communicating with Backend

```bash
# Check CORS is enabled
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  http://localhost:8000/api/v1/chat/message -v

# Check API_URL in frontend
# File: frontend/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Problem: High Memory Usage

```bash
# Check memory
docker stats

# Reduce Ollama memory
# Edit docker-compose.yml, set:
# deploy:
#   resources:
#     limits:
#       memory: 2G

docker-compose up -d
```

---

## 📊 VERIFY DEPLOYMENT

### Checklist

- [ ] Frontend loads at http://localhost:3000
- [ ] API docs available at http://localhost:8000/docs
- [ ] Can create user account
- [ ] Can login with credentials
- [ ] Chat responds to messages
- [ ] Can upload documents
- [ ] OCR processing starts
- [ ] Admin dashboard accessible
- [ ] No errors in docker logs

### Check Status Command

```bash
# All services running
docker-compose ps

# Should show:
# STATUS: Up (or Up X seconds)
# for all services

# Check logs for errors
docker-compose logs | grep -i error
```

---

## 🚀 NEXT STEPS

### 1. Populate Knowledge Base

```bash
# Add FAQs to system
# Edit: backend/app/data/default_faqs.py
# Add your college FAQs

# Restart backend
docker-compose restart backend
```

### 2. Customize for Your College

Edit `backend/config/settings.py`:
```python
COLLEGE_NAME = "Your College Name"
COLLEGE_CITY = "Your City"
ADMISSION_EMAIL = "admissions@yourcollegename.edu"
```

### 3. Create Admin Account

```bash
# Via API with special admin flag
# Or via database directly
```

### 4. Load Sample Students (Optional)

```bash
cd backend
python app/seed.py  # Creates 10 test students
```

### 5. Run Tests

```bash
cd backend
pytest
```

---

## 📞 SUPPORT

**Local Issues?**
- Check logs: `docker-compose logs [service-name]`
- Restart service: `docker-compose restart [service-name]`
- Full restart: `docker-compose down && docker-compose up -d`

**Deployment Questions?**
- See: `DEPLOYMENT_GUIDE.md`
- See: `IMPLEMENTATION_GUIDE.md`

**Institutional Setup?**
- See: `INSTITUTIONAL_ROLLOUT_PLAN.md`

---

**Your system is ready! 🎉**

---

## COMMAND REFERENCE

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend

# Restart service
docker-compose restart backend

# Execute command in container
docker-compose exec backend bash

# Remove all data (WARNING!)
docker-compose down -v

# View configuration
docker-compose config

# Check service health
docker-compose ps
```

### Useful URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Student Interface |
| Backend API | http://localhost:8000 | API Server |
| API Docs | http://localhost:8000/docs | Swagger Documentation |
| Ollama | http://localhost:11434 | LLM Service |
| Redis | localhost:6379 | Cache |
| PostgreSQL | localhost:5432 | Database |
| Qdrant | http://localhost:6333 | Vector DB |

---

**Ready to onboard students? Let's go! 🚀**
