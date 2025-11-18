# Deployment Guide

## Deployment Options

### 1. Docker Compose (Recommended for Development)

```bash
# Clone repository
git clone <repo_url>
cd agri-chatbot

# Copy environment template
cp backend/.env.example backend/.env

# Edit .env with your credentials
nano backend/.env

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: localhost:5432

---

### 2. Railway.app Deployment

#### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with code

#### Steps

1. **Push code to GitHub**

2. **In Railway Dashboard:**
   - New Project
   - Select "Deploy from GitHub"
   - Select your repository

3. **Add Services:**

   **PostgreSQL:**
   - Add from template
   - Copy DATABASE_URL

   **Python Backend:**
   - Add empty service
   - Connect to GitHub repo
   - Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from .env
   - Add DATABASE_URL from PostgreSQL

   **Node.js Frontend:**
   - Add empty service
   - Connect to GitHub repo
   - Set start command: `npm run build && npm start`
   - Add REACT_APP_API_URL pointing to backend

4. **Deploy**
   - Click Deploy
   - Monitor logs in Railway dashboard

#### Accessing Application
- Backend: https://<project>.railway.app
- Frontend: https://<project>-frontend.railway.app

---

### 3. Render.com Deployment

#### Prerequisites
- Render account (https://render.com)
- GitHub repository

#### Steps

1. **PostgreSQL Database:**
   - New → PostgreSQL
   - Name: agri-chatbot-db
   - Create database

2. **Backend Service:**
   - New → Web Service
   - Connect GitHub repo
   - Environment: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - DATABASE_URL (from PostgreSQL)
     - OPENAI_API_KEY
     - AFRICAS_TALKING_API_KEY
     - AFRICAS_TALKING_USERNAME
     - WEATHER_API_KEY

3. **Frontend Service:**
   - New → Static Site
   - Connect GitHub repo (frontend folder)
   - Build command: `npm install && npm run build`
   - Publish directory: `build`
   - Add environment:
     - REACT_APP_API_URL pointing to backend

---

### 4. AWS EC2 Deployment

#### Prerequisites
- AWS account
- EC2 instance (t2.small or larger)
- Ubuntu 22.04 LTS

#### Setup

```bash
# SSH into instance
ssh -i key.pem ubuntu@<instance_ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <repo_url>
cd agri-chatbot

# Setup environment
cp backend/.env.example backend/.env
nano backend/.env  # Add your credentials

# Start services
sudo docker-compose up -d

# Setup Nginx reverse proxy
sudo apt install nginx -y

# Configure Nginx (see nginx.conf below)
# Enable and start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/agri-chatbot`:

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name _;

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable configuration:
```bash
sudo ln -s /etc/nginx/sites-available/agri-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 5. Azure Container Instances

#### Prerequisites
- Azure account
- Azure CLI installed
- Docker image built and pushed to Docker Hub

#### Steps

```bash
# Build Docker images
docker build -t <dockerhub_user>/agri-backend:latest ./backend
docker build -t <dockerhub_user>/agri-frontend:latest ./frontend

# Push to Docker Hub
docker push <dockerhub_user>/agri-backend:latest
docker push <dockerhub_user>/agri-frontend:latest

# Create Azure resource group
az group create --name agri-chatbot-rg --location eastus

# Create container instances
az container create \
  --resource-group agri-chatbot-rg \
  --name agri-backend \
  --image <dockerhub_user>/agri-backend:latest \
  --cpu 1 \
  --memory 1 \
  --ports 8000 \
  --environment-variables DATABASE_URL=$DATABASE_URL OPENAI_API_KEY=$OPENAI_API_KEY

az container create \
  --resource-group agri-chatbot-rg \
  --name agri-frontend \
  --image <dockerhub_user>/agri-frontend:latest \
  --cpu 1 \
  --memory 1 \
  --ports 3000 \
  --environment-variables REACT_APP_API_URL=$API_URL
```

---

## Production Checklist

- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Configure HTTPS/SSL certificate
- [ ] Set ALLOWED_ORIGINS to your domain only
- [ ] Enable database backups
- [ ] Setup monitoring and alerting
- [ ] Configure email for error notifications
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] API authentication implemented
- [ ] Database encrypted
- [ ] Environment variables secured
- [ ] CDN configured for static assets
- [ ] Database connection pooling enabled
- [ ] Logging centralized
- [ ] Health checks monitoring

---

## SSL/TLS Certificate Setup

### Using Let's Encrypt with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot certonly --nginx -d agri-chatbot.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test renewal
sudo certbot renew --dry-run
```

### Update Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    
    ssl_certificate /etc/letsencrypt/live/agri-chatbot.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/agri-chatbot.example.com/privkey.pem;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name agri-chatbot.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoring & Logging

### Application Logs

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Export logs
docker-compose logs backend > backend.log
```

### Database Backups

```bash
# Backup
docker-compose exec postgres pg_dump -U agri_user agri_chatbot > backup.sql

# Restore
docker-compose exec -T postgres psql -U agri_user agri_chatbot < backup.sql
```

### Monitoring Tools
- Grafana + Prometheus for metrics
- ELK Stack for log aggregation
- Sentry for error tracking
- Uptime Robot for uptime monitoring

---

## Scaling

### Horizontal Scaling
- Load balancer in front of multiple backend instances
- Separate database read replicas
- Redis caching layer
- CDN for static content

### Vertical Scaling
- Increase server CPU/RAM
- Optimize database queries
- Add connection pooling
- Cache frequently accessed data

---

## Troubleshooting

### Backend won't start
```bash
# Check database connection
docker-compose logs postgres

# Check environment variables
docker-compose exec backend env | grep DATABASE_URL

# Run migrations
docker-compose exec backend alembic upgrade head
```

### Frontend not loading
```bash
# Check API URL
docker-compose exec frontend cat .env

# Check build
docker-compose logs frontend
```

### Database connection issues
```bash
# Connect to database directly
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# Check tables
\dt

# Check data
SELECT COUNT(*) FROM farmers;
```

---

**Last Updated**: November 2025
