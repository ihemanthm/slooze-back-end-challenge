# 🚀 Deployment Guide - Slooze Food Ordering API

## 🐳 Docker Deployment

### Quick Start with Docker Compose

**1. Build and start all services:**
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

**2. Check status:**
```bash
docker-compose -f docker-compose.prod.yml ps
```

**3. View logs:**
```bash
docker-compose -f docker-compose.prod.yml logs -f api
```

**4. Access the API:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**5. Stop services:**
```bash
docker-compose -f docker-compose.prod.yml down
```

---

## 🔧 Manual Docker Build

### Build the Docker Image

```bash
# Build the image
docker build -t slooze-api:latest .

# Check image size
docker images | grep slooze-api
```

### Run the Container

```bash
# Run with environment variables
docker run -d \
  --name slooze-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SECRET_KEY="your-secret-key" \
  slooze-api:latest
```

### Run Migrations

```bash
# Run migrations inside container
docker exec slooze-api alembic upgrade head

# Seed database
docker exec slooze-api python scripts/seed_data.py
```

---

## 🌐 Production Deployment Options

### Option 1: Docker Compose (Recommended for VPS)

**Prerequisites:**
- Docker & Docker Compose installed
- Domain name (optional)
- SSL certificate (for HTTPS)

**Steps:**

1. **Clone repository:**
```bash
git clone <your-repo-url>
cd slooze-backend-challenge
```

2. **Create production environment file:**
```bash
cp .env.example .env.prod
```

3. **Edit `.env.prod`:**
```env
POSTGRES_USER=slooze_user
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=slooze_db
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql://slooze_user:<strong-password>@postgres:5432/slooze_db
```

4. **Deploy:**
```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

5. **Setup reverse proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### Option 2: Kubernetes Deployment

**Create Kubernetes manifests:**

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: slooze-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: slooze-api
  template:
    metadata:
      labels:
        app: slooze-api
    spec:
      containers:
      - name: api
        image: slooze-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: slooze-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: slooze-secrets
              key: secret-key
---
apiVersion: v1
kind: Service
metadata:
  name: slooze-api-service
spec:
  selector:
    app: slooze-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Deploy to Kubernetes:**
```bash
kubectl apply -f deployment.yaml
```

---

### Option 3: Cloud Platform Deployment

#### **AWS ECS/Fargate**

1. **Push image to ECR:**
```bash
aws ecr create-repository --repository-name slooze-api
docker tag slooze-api:latest <account-id>.dkr.ecr.<region>.amazonaws.com/slooze-api:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/slooze-api:latest
```

2. **Create ECS task definition and service**

#### **Google Cloud Run**

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/<project-id>/slooze-api

# Deploy to Cloud Run
gcloud run deploy slooze-api \
  --image gcr.io/<project-id>/slooze-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### **Azure Container Instances**

```bash
# Push to ACR
az acr build --registry <registry-name> --image slooze-api:latest .

# Deploy to ACI
az container create \
  --resource-group <resource-group> \
  --name slooze-api \
  --image <registry-name>.azurecr.io/slooze-api:latest \
  --dns-name-label slooze-api \
  --ports 8000
```

#### **Heroku**

```bash
# Login to Heroku
heroku login
heroku container:login

# Create app
heroku create slooze-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
heroku container:push web
heroku container:release web

# Run migrations
heroku run alembic upgrade head
heroku run python scripts/seed_data.py
```

---

## 🔐 Security Checklist

### Before Production Deployment

- [ ] **Change SECRET_KEY** to a cryptographically secure random value
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- [ ] **Use strong database password**
  ```bash
  openssl rand -base64 32
  ```

- [ ] **Enable HTTPS/TLS** with valid SSL certificate

- [ ] **Configure CORS** for specific origins only
  ```python
  # In app/main.py
  origins = [
      "https://yourdomain.com",
      "https://app.yourdomain.com",
  ]
  ```

- [ ] **Set secure environment variables** (never commit to Git)

- [ ] **Enable database backups** (automated daily backups)

- [ ] **Implement rate limiting** (e.g., using slowapi)

- [ ] **Setup monitoring** (e.g., Sentry, DataDog)

- [ ] **Configure logging** to external service

- [ ] **Review and update dependencies** regularly

---

## 📊 Monitoring & Logging

### Health Check Endpoint

The Docker image includes a health check that pings the API:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' slooze-api
```

### View Logs

```bash
# Docker Compose
docker-compose -f docker-compose.prod.yml logs -f api

# Docker
docker logs -f slooze-api

# Kubernetes
kubectl logs -f deployment/slooze-api
```

### Metrics

Add Prometheus metrics (optional):

```bash
pip install prometheus-fastapi-instrumentator
```

```python
# In app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t slooze-api:latest .
    
    - name: Run tests
      run: |
        docker-compose up -d postgres
        docker run --network host slooze-api:latest pytest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag slooze-api:latest ${{ secrets.DOCKER_USERNAME }}/slooze-api:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/slooze-api:latest
```

---

## 🧪 Testing Docker Build

### Test locally before deploying:

```bash
# Build
docker build -t slooze-api:test .

# Run with test database
docker run -d --name test-postgres -e POSTGRES_PASSWORD=test postgres:15-alpine
docker run --link test-postgres:postgres \
  -e DATABASE_URL="postgresql://postgres:test@postgres:5432/postgres" \
  -p 8000:8000 \
  slooze-api:test

# Run tests
docker exec <container-id> pytest -v

# Cleanup
docker stop test-postgres slooze-api
docker rm test-postgres slooze-api
```

---

## 📦 Image Optimization

The Dockerfile uses multi-stage builds for:
- ✅ Smaller final image size (~200MB vs ~1GB)
- ✅ Faster builds with layer caching
- ✅ Security (non-root user)
- ✅ Production-ready dependencies only

**Check image size:**
```bash
docker images slooze-api
```

---

## 🆘 Troubleshooting

### Container won't start

```bash
# Check logs
docker logs slooze-api

# Check if port is in use
lsof -i :8000

# Restart container
docker restart slooze-api
```

### Database connection issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Test connection
docker exec slooze-api python -c "from app.db.session import engine; engine.connect()"
```

### Migrations failing

```bash
# Run migrations manually
docker exec slooze-api alembic upgrade head

# Check migration status
docker exec slooze-api alembic current
```

---

## 🎯 Production Checklist

- [ ] Docker image builds successfully
- [ ] All tests pass in container
- [ ] Health check endpoint works
- [ ] Database migrations run automatically
- [ ] Environment variables configured
- [ ] SSL/TLS enabled
- [ ] CORS configured properly
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Documentation updated

---

**Your API is now ready for production deployment! 🚀**
