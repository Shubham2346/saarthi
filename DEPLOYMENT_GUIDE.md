# SMART STUDENT ONBOARDING AGENT - DEPLOYMENT GUIDE

**Complete Production Deployment Instructions**  
**Version:** 1.0.0  
**Last Updated:** May 13, 2026

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Configuration](#production-configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Database Migration](#database-migration)
8. [Load Testing](#load-testing)
9. [Monitoring & Logging](#monitoring--logging)
10. [Rollback Procedures](#rollback-procedures)

---

## Pre-Deployment Checklist

### Security
- [ ] JWT_SECRET_KEY changed from default
- [ ] Google OAuth credentials obtained
- [ ] HTTPS/SSL certificates generated
- [ ] Database password changed
- [ ] Firewall rules configured
- [ ] CORS origins whitelisted
- [ ] API rate limiting enabled
- [ ] Admin credentials secure

### Performance
- [ ] Database indexes created
- [ ] Vector DB indexed
- [ ] Redis cache configured
- [ ] CDN configured for static assets
- [ ] Database connection pooling
- [ ] API response time optimized
- [ ] Load tested (100+ users)
- [ ] Memory/CPU limits set

### Functionality
- [ ] All agents tested
- [ ] Document upload tested
- [ ] OCR accuracy verified
- [ ] Escalation workflow tested
- [ ] Email notifications working (if configured)
- [ ] Admin dashboard functional
- [ ] Analytics tracking enabled
- [ ] Error handling verified

### Documentation
- [ ] README updated
- [ ] API documentation current
- [ ] Deployment procedure documented
- [ ] Disaster recovery plan ready
- [ ] Support contact info configured
- [ ] User onboarding guide ready

---

## Local Development Setup

### 1. System Preparation

```bash
# Install required tools
## macOS
brew install python@3.11 node postgresql redis-server docker

## Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv nodejs postgresql-15 \
  redis-server docker.io docker-compose tesseract-ocr

## Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installations
python3.11 --version  # Python 3.11+
node --version        # Node 18+
docker --version      # Docker 24+
ollama --version      # Ollama
```

### 2. Clone & Setup Repository

```bash
# Clone repository
git clone https://github.com/your-org/saarthi.git
cd saarthi

# Create local environment file
cat > .env.local << 'EOF'
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./saarthi.db
FRONTEND_URL=http://localhost:3000
OLLAMA_BASE_URL=http://localhost:11434
EOF
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1' > .env.local

# Run development server
npm run dev
# Frontend: http://localhost:3000
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 5. Ollama Setup

```bash
# Start Ollama service
ollama serve

# In another terminal, pull models
ollama pull llama2        # Main language model
ollama pull llava         # Vision model for documents

# Test Ollama
curl http://localhost:11434/api/tags
```

### 6. Database Initialization (PostgreSQL for Staging/Prod)

```bash
# Install PostgreSQL (if not done)
# Create database and user
psql -U postgres << 'EOF'
CREATE DATABASE saarthi_db;
CREATE USER saarthi_user WITH PASSWORD 'your_secure_password';
ALTER ROLE saarthi_user SET client_encoding TO 'utf8';
ALTER ROLE saarthi_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE saarthi_db TO saarthi_user;
EOF

# Update DATABASE_URL in .env
DATABASE_URL="postgresql+asyncpg://saarthi_user:your_secure_password@localhost:5432/saarthi_db"

# Run migrations
alembic upgrade head
```

---

## Docker Deployment

### 1. Build Docker Images

```bash
# Build backend image
cd backend
docker build -f deployment/docker/Dockerfile -t saarthi/backend:latest .

# Build frontend image (if custom Dockerfile)
cd ../frontend
docker build -t saarthi/frontend:latest .
```

### 2. Docker Compose - Development

```bash
cd backend/deployment/docker

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend  # Or 'frontend', 'postgres', 'ollama'

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Ollama: http://localhost:11434
```

### 3. Docker Compose - Production

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Configure secrets
docker secret create db_password db_password.txt
docker secret create jwt_secret jwt_secret.txt

# Scale services
docker-compose up -d --scale backend=3
```

### 4. Docker Network Management

```bash
# Create custom network
docker network create saarthi-network

# Connect containers
docker network connect saarthi-network container_name

# Inspect network
docker network inspect saarthi-network
```

---

## Kubernetes Deployment

### 1. Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Setup kubeconfig
export KUBECONFIG=/path/to/kubeconfig.yaml

# Verify cluster access
kubectl cluster-info
```

### 2. Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace saarthi

# Create secrets
kubectl create secret generic saarthi-secrets \
  --from-literal=jwt-secret-key='your-super-secret-key' \
  --from-literal=db-password='your-db-password' \
  -n saarthi

# Create image pull secret (if using private registry)
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=username \
  --docker-password=password \
  -n saarthi
```

### 3. Apply Kubernetes Manifests

```bash
# Apply manifest
kubectl apply -f backend/deployment/kubernetes/k8s-manifest.yaml

# Verify deployment
kubectl get all -n saarthi

# Check pod status
kubectl get pods -n saarthi -w

# View pod logs
kubectl logs deployment/backend -n saarthi -f
```

### 4. Expose Services

```bash
# Get service details
kubectl get services -n saarthi

# Port forwarding for testing
kubectl port-forward svc/backend-service 8000:8000 -n saarthi
kubectl port-forward svc/frontend-service 3000:3000 -n saarthi

# Setup Ingress for external access
kubectl apply -f ingress.yaml -n saarthi
```

### 5. Check Pod Logs & Debugging

```bash
# View recent logs
kubectl logs <pod-name> -n saarthi

# Stream logs
kubectl logs <pod-name> -n saarthi -f

# Describe pod (for events)
kubectl describe pod <pod-name> -n saarthi

# Execute command in pod
kubectl exec -it <pod-name> -n saarthi -- /bin/bash
```

---

## Production Configuration

### 1. Environment Variables

```bash
# backend/.env (Production)
APP_ENV=production
DEBUG=false
JWT_SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_urlsafe(32))">
DATABASE_URL=postgresql+asyncpg://saarthi_user:${DB_PASSWORD}@db.example.com:5432/saarthi_db
FRONTEND_URL=https://app.example.com
OLLAMA_BASE_URL=http://ollama-gpu-server:11434
REDIS_URL=redis://redis-server:6379
VECTOR_DB_TYPE=qdrant
QDRANT_URL=http://qdrant-server:6333

# Google OAuth
GOOGLE_CLIENT_ID=<your-client-id>.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=<your-client-secret>

# Email notifications (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=<app-specific-password>

# Sentry error tracking (optional)
SENTRY_DSN=<your-sentry-dsn>
```

### 2. SSL/TLS Certificate Generation

```bash
# Using Let's Encrypt with Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d app.example.com -d www.example.com

# Configure auto-renewal
sudo certbot renew --dry-run

# Update nginx to use certificate
sudo vim /etc/nginx/sites-available/default
# ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
```

### 3. Nginx Configuration

```bash
# Copy nginx config
sudo cp backend/deployment/nginx/nginx.conf /etc/nginx/sites-available/saarthi

# Enable site
sudo ln -s /etc/nginx/sites-available/saarthi /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 4. Database Backup Strategy

```bash
# Create backup directory
mkdir -p /backups/postgres

# Automated daily backup script
cat > /etc/cron.daily/saarthi-backup << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -U saarthi_user saarthi_db > $BACKUP_DIR/saarthi_$TIMESTAMP.sql
# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
EOF

chmod +x /etc/cron.daily/saarthi-backup
```

---

## SSL/TLS Setup

### 1. Self-Signed Certificate (Testing)

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### 2. Let's Encrypt Production Certificate

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --nginx -d app.example.com

# Configure auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check renewal status
sudo certbot renew --dry-run
```

### 3. Update Nginx Configuration

```nginx
# In /etc/nginx/sites-available/saarthi
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of config
}
```

---

## Database Migration

### 1. Schema Initialization

```bash
# Using Alembic for migrations
cd backend

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Check current revision
alembic current
```

### 2. Data Migration

```bash
# Backup existing data
pg_dump saarthi_db > saarthi_backup.sql

# Run migration
python scripts/migrate_data.py

# Verify data
psql saarthi_db -c "SELECT COUNT(*) FROM users;"
```

---

## Load Testing

### 1. Using Apache Bench

```bash
# Single endpoint test
ab -n 1000 -c 100 http://localhost:8000/api/v1/health

# POST request test
ab -n 1000 -c 100 -p payload.json -T application/json \
  http://localhost:8000/api/v1/chat/message
```

### 2. Using Locust

```bash
# Create load test script
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def chat_message(self):
        self.client.post("/api/v1/chat/message",
            json={"student_id": "123", "message": "What's my task?"})
EOF

# Run load test
locust -f locustfile.py -u 100 -r 10 -t 5m
```

---

## Monitoring & Logging

### 1. Prometheus Setup

```bash
# Configuration
cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['localhost:8000']
EOF

# Run Prometheus
docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

### 2. Grafana Dashboards

```bash
# Run Grafana
docker run -d -p 3001:3000 grafana/grafana

# Access: http://localhost:3001
# Add Prometheus as data source
# Import dashboard templates
```

### 3. Log Aggregation

```bash
# Using ELK Stack (Elasticsearch, Logstash, Kibana)
docker-compose up -d elasticsearch logstash kibana

# Configure app logging to send to Logstash
# Access Kibana: http://localhost:5601
```

---

## Rollback Procedures

### Docker Rollback

```bash
# Stop current services
docker-compose down

# Start previous version
docker-compose -f docker-compose.v1.0.0.yml up -d

# Verify
docker-compose ps
```

### Kubernetes Rollback

```bash
# Check rollout history
kubectl rollout history deployment/backend -n saarthi

# Rollback to previous version
kubectl rollout undo deployment/backend -n saarthi

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=1 -n saarthi

# Monitor rollback
kubectl rollout status deployment/backend -n saarthi
```

### Database Rollback

```bash
# List available backups
ls -la /backups/postgres/

# Restore from backup
psql saarthi_db < /backups/postgres/saarthi_20260513_120000.sql

# Verify data
psql saarthi_db -c "SELECT COUNT(*) FROM users;"
```

---

## Troubleshooting Production Issues

### Issue: High API Latency

```bash
# Check database performance
psql saarthi_db -c "SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Check Redis
redis-cli info stats

# Increase connection pool size in DATABASE_URL
DATABASE_URL="postgresql+asyncpg://user:pass@host/db?min_size=20&max_size=50"
```

### Issue: Out of Memory

```bash
# Check memory usage
docker stats

# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4G
    reservations:
      memory: 2G
```

### Issue: Ollama Timeout

```bash
# Check Ollama status
curl http://ollama:11434/api/tags

# Increase timeout in settings.py
AGENT_TIMEOUT=60
LLM_TIMEOUT=120
```

---

## Production Checklist Summary

- [ ] All services running and healthy
- [ ] Database backups working
- [ ] SSL/TLS certificates valid
- [ ] Monitoring and alerting active
- [ ] Log aggregation working
- [ ] Load balancing configured
- [ ] Rate limiting enabled
- [ ] Error tracking (Sentry) active
- [ ] Admin dashboard accessible
- [ ] API documentation deployed
- [ ] Support contacts configured
- [ ] Escalation procedures tested
- [ ] Performance baseline established
- [ ] Security audit completed
- [ ] Documentation updated

---

**Deployment Complete!**

Your Smart Student Onboarding Agent is now ready for institutional use.

For 24/7 support: support@example.com  
Status Page: https://status.example.com
