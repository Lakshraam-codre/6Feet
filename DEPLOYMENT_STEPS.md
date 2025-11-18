# Agriculture Extension Chatbot - Step-by-Step Deployment Guide

## 🚀 Complete Deployment Instructions

This guide will walk you through deploying the Agriculture Extension Chatbot to production.

---

## OPTION 1: Deploy Using Docker Compose (Local/VPS)

### Prerequisites
- Docker installed
- Docker Compose installed
- 2GB RAM minimum
- 10GB disk space

### Step 1: Get API Keys (Required - 15 minutes)

#### 1.1 OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Save it securely

#### 1.2 Africa's Talking Account
1. Go to https://africastalking.com
2. Create account (free)
3. Go to Dashboard → Settings
4. Note your API Key and Username
5. Enable Sandbox mode for testing

#### 1.3 Weather API Key
1. Go to https://openweathermap.org/api
2. Sign up (free tier available)
3. Click "API keys" in dashboard
4. Copy your default API key
5. Save it

### Step 2: Download and Setup (10 minutes)

```bash
# Option A: If you have the project already
cd C:\Users\laksh\OneDrive\Desktop\googleai

# Option B: Clone from GitHub (if deployed there)
git clone https://github.com/yourusername/agri-chatbot.git
cd agri-chatbot
```

### Step 3: Configure Environment (5 minutes)

```bash
# Navigate to backend folder
cd backend

# Copy environment template
cp .env.example .env

# Windows equivalent:
# copy .env.example .env

# Edit the .env file
# nano .env  # Linux/Mac
# or
# notepad .env  # Windows
```

### Step 4: Add Your API Keys to .env

Open `backend/.env` and fill in:

```env
# Database (keep as-is for Docker)
DATABASE_URL=postgresql://agri_user:agri_password@postgres:5432/agri_chatbot

# LLM - PASTE YOUR OPENAI KEY HERE
OPENAI_API_KEY=sk-your_actual_key_here

# Africa's Talking - PASTE YOUR CREDENTIALS HERE
AFRICAS_TALKING_API_KEY=your_actual_africas_talking_key
AFRICAS_TALKING_USERNAME=your_actual_username
SMS_SHORTCODE=lesotho_agri
USSD_CODE=*384*50234#

# Weather API - PASTE YOUR KEY HERE
WEATHER_API_KEY=your_actual_weather_api_key
WEATHER_PROVIDER=openweather

# Deployment settings
DEBUG=False
SECRET_KEY=change-this-to-a-random-string-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Step 5: Start Services (5 minutes)

```bash
# Go to root directory
cd ..

# Build and start containers
docker-compose up -d

# Wait 30 seconds for services to start

# Check status
docker-compose ps

# Expected output:
# NAME          STATUS
# postgres      Up 1 minute
# backend       Up 30 seconds
# frontend      Up 30 seconds
```

### Step 6: Verify Installation (10 minutes)

#### Test Backend
```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"Agriculture Extension Chatbot - Lesotho","version":"1.0.0"}
```

#### Test Frontend
```bash
# Open in browser
http://localhost:3000

# You should see the chat interface
```

#### Test Database
```bash
# Connect to database
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# Run command:
SELECT COUNT(*) FROM farmers;

# Should return: 0 (empty table is normal)

# Exit:
\q
```

### Step 7: Add Test Data (10 minutes)

#### Add a Test Farmer
```bash
curl -X POST http://localhost:8000/api/admin/farmers \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+266123456789",
    "location": "Maseru",
    "name": "Test Farmer",
    "language_preference": "english",
    "literacy_level": "basic",
    "farming_experience": "beginner",
    "primary_crop": "maize",
    "farm_size_hectares": 0.5,
    "soil_type": "loamy"
  }'

# You should get back the farmer with ID: 1
```

#### Add Market Price
```bash
curl -X POST http://localhost:8000/api/admin/market-prices \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "maize",
    "location": "Maseru",
    "price_per_kg": 3.50,
    "currency": "LSL",
    "demand_level": "high",
    "best_selling_period": "May-July",
    "source": "manual"
  }'
```

### Step 8: Test Chat Functionality (5 minutes)

#### Via Web Interface
1. Open http://localhost:3000
2. Type: "How do I grow maize?"
3. Should get response from chatbot

#### Via API
```bash
curl -X POST http://localhost:8000/api/channels/web/chat \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": 1,
    "message": "How do I prevent fall armyworm?",
    "channel": "web",
    "language": "english"
  }'
```

### Step 9: Check Logs for Issues

```bash
# View all logs
docker-compose logs

# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# View database logs
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f backend
```

### Step 10: Your Application is Running! 🎉

**Access Points:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

---

## OPTION 2: Deploy to Railway.app (Easiest Cloud Option)

Railway is recommended for beginners - it's free tier friendly and very easy.

### Step 1: Prepare Repository (10 minutes)

```bash
# If not already a git repo
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
# Create new repo on GitHub.com
# Then:
git remote add origin https://github.com/yourusername/agri-chatbot.git
git push -u origin main
```

### Step 2: Create Railway Account (5 minutes)

1. Go to https://railway.app
2. Click "Start Project"
3. Choose "Deploy from GitHub"
4. Authorize Railway to access GitHub
5. Select your repository

### Step 3: Add PostgreSQL (5 minutes)

1. In Railway Dashboard
2. Click "New"
3. Select "PostgreSQL"
4. Railway will create the database
5. Copy the database URL for next step

### Step 4: Deploy Backend (10 minutes)

1. Click "New"
2. Select "GitHub Repo"
3. Choose your repository
4. Set Variables:
   ```
   OPENAI_API_KEY=your_key
   AFRICAS_TALKING_API_KEY=your_key
   AFRICAS_TALKING_USERNAME=your_username
   WEATHER_API_KEY=your_key
   DATABASE_URL=postgresql://... (from PostgreSQL)
   DEBUG=False
   ```
5. Set Root Directory: `backend`
6. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Deploy

### Step 5: Deploy Frontend (10 minutes)

1. Click "New"
2. Select "GitHub Repo"
3. Choose your repository
4. Set Variables:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app/api
   ```
5. Set Root Directory: `frontend`
6. Set Build Command: `npm install && npm run build`
7. Set Start Command: `npm start`
8. Deploy

### Step 6: Get URLs

- Backend URL: https://your-project-backend.railway.app
- Frontend URL: https://your-project-frontend.railway.app

### Step 7: Test Deployment

```bash
# Test backend
curl https://your-project-backend.railway.app/health

# Test frontend
# Open in browser: https://your-project-frontend.railway.app
```

---

## OPTION 3: Deploy to Render.com (Alternative Cloud)

### Step 1: Prepare Repository

Same as Railway Step 1 - push code to GitHub

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up
3. Connect GitHub account

### Step 3: Deploy PostgreSQL

1. Dashboard → New
2. Select "PostgreSQL"
3. Set name: `agri-chatbot-db`
4. Copy connection string

### Step 4: Deploy Backend

1. Dashboard → New → Web Service
2. Connect GitHub repo
3. Set buildCommand: `pip install -r requirements.txt`
4. Set startCommand: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set Root Directory: `backend`
6. Add Environment Variables (same as Railway)
7. Deploy

### Step 5: Deploy Frontend

1. Dashboard → New → Static Site
2. Connect GitHub repo
3. Set Root Directory: `frontend`
4. Set Build Command: `npm install && npm run build`
5. Set Publish Directory: `build`
6. Deploy

---

## OPTION 4: Deploy to AWS EC2 (Most Control)

### Step 1: Launch EC2 Instance (10 minutes)

1. Go to AWS Console
2. EC2 → Launch Instance
3. Choose: Ubuntu 22.04 LTS
4. Instance Type: t2.micro or t2.small
5. Storage: 20GB
6. Create key pair, download .pem file
7. Create security group:
   - Allow SSH (port 22)
   - Allow HTTP (port 80)
   - Allow HTTPS (port 443)
8. Launch instance

### Step 2: Connect to Instance (5 minutes)

```bash
# On your computer
ssh -i "your-key.pem" ubuntu@your-instance-ip

# Replace:
# - your-key.pem with your actual key file path
# - your-instance-ip with actual instance public IP
```

### Step 3: Update System (5 minutes)

```bash
# Update packages
sudo apt update
sudo apt upgrade -y

# Install required software
sudo apt install -y git curl
```

### Step 4: Install Docker (10 minutes)

```bash
# Download Docker install script
curl -fsSL https://get.docker.com -o get-docker.sh

# Run script
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Logout and login again for changes to take effect
exit
```

### Step 5: Install Docker Compose (5 minutes)

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 6: Clone Project (5 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/agri-chatbot.git
cd agri-chatbot

# Or if local:
# Copy files to server using SCP
scp -i "your-key.pem" -r ./agri-chatbot ubuntu@your-instance-ip:~
```

### Step 7: Configure Environment (5 minutes)

```bash
cd agri-chatbot

# Copy template
cp backend/.env.example backend/.env

# Edit with your keys
nano backend/.env

# Add all API keys (see Step 4 from Option 1)
```

### Step 8: Start Services (5 minutes)

```bash
# Start Docker services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 9: Setup Nginx Reverse Proxy (15 minutes)

```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/agri-chatbot

# Paste this configuration:
```

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable configuration
sudo ln -s /etc/nginx/sites-available/agri-chatbot /etc/nginx/sites-enabled/

# Test Nginx
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 10: Setup SSL Certificate (10 minutes)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Update Nginx config to use SSL
# Edit: sudo nano /etc/nginx/sites-available/agri-chatbot
# Add SSL configuration

# Test renewal
sudo certbot renew --dry-run
```

### Step 11: Your App is Live! 🎉

- Access at: `https://your-domain.com`
- API at: `https://your-domain.com/api`

---

## OPTION 5: Deploy to Azure Container Instances

### Step 1: Build Docker Images

```bash
# Navigate to project
cd agri-chatbot

# Build backend image
docker build -t agri-backend:latest ./backend

# Build frontend image
docker build -t agri-frontend:latest ./frontend

# Tag for Azure Container Registry
docker tag agri-backend:latest your-registry.azurecr.io/agri-backend:latest
docker tag agri-frontend:latest your-registry.azurecr.io/agri-frontend:latest
```

### Step 2: Push to Azure Container Registry

```bash
# Login to Azure
az login

# Create resource group
az group create --name agri-chatbot-rg --location eastus

# Create container registry
az acr create --resource-group agri-chatbot-rg --name yourregistry --sku Basic

# Login to registry
az acr login --name yourregistry

# Push images
docker push your-registry.azurecr.io/agri-backend:latest
docker push your-registry.azurecr.io/agri-frontend:latest
```

### Step 3: Deploy with Azure Container Instances

```bash
# Deploy backend
az container create \
  --resource-group agri-chatbot-rg \
  --name agri-backend \
  --image your-registry.azurecr.io/agri-backend:latest \
  --cpu 1 --memory 1 \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL="postgresql://..." \
    OPENAI_API_KEY="sk-..." \
  --registry-login-server your-registry.azurecr.io \
  --registry-username username \
  --registry-password password

# Deploy frontend
az container create \
  --resource-group agri-chatbot-rg \
  --name agri-frontend \
  --image your-registry.azurecr.io/agri-frontend:latest \
  --cpu 1 --memory 1 \
  --ports 3000 \
  --environment-variables \
    REACT_APP_API_URL="http://backend-ip:8000/api"
```

---

## Post-Deployment Configuration

### Step 1: Configure Africa's Talking Callbacks (15 minutes)

1. Go to Africa's Talking Dashboard
2. Settings → SMS Webhooks
3. Add Callback URL:
   ```
   https://your-deployment-url/api/channels/sms/webhook
   ```
4. Settings → USSD Webhooks
5. Add Callback URL:
   ```
   https://your-deployment-url/api/channels/ussd/webhook
   ```
6. Test with SMS to your shortcode

### Step 2: Add Farmers & Prices (20 minutes)

```bash
# Add test farmers
curl -X POST https://your-deployment-url/api/admin/farmers \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+266123456789",
    "location": "Maseru",
    "name": "Farmer Name",
    "language_preference": "english",
    "primary_crop": "maize"
  }'

# Add market prices for main crops
for crop in maize wheat beans potatoes cabbage; do
  curl -X POST https://your-deployment-url/api/admin/market-prices \
    -H "Content-Type: application/json" \
    -d "{
      \"crop_name\": \"$crop\",
      \"location\": \"Maseru\",
      \"price_per_kg\": 3.50,
      \"currency\": \"LSL\",
      \"demand_level\": \"medium\"
    }"
done
```

### Step 3: Setup Monitoring (Optional - 30 minutes)

```bash
# If using AWS:
# - Setup CloudWatch alarms
# - Enable CloudTrail logging
# - Configure SNS notifications

# If using other platforms:
# - Setup health check monitoring
# - Enable application logs
# - Configure alert notifications
```

### Step 4: Setup Database Backups (10 minutes)

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T postgres pg_dump -U agri_user agri_chatbot > $BACKUP_DIR/backup_$TIMESTAMP.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

# Make executable
chmod +x backup.sh

# Schedule with cron (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## Troubleshooting Deployment Issues

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database not ready - wait 30 seconds
# 2. API keys not set - check .env file
# 3. Port in use - change port in docker-compose.yml

# Restart
docker-compose restart backend
```

### Frontend Blank/Error

```bash
# Check logs
docker-compose logs frontend

# Check API URL
docker-compose exec frontend cat .env

# Make sure REACT_APP_API_URL points to backend
```

### Database Connection Error

```bash
# Connect directly
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# If fails, reset database
docker-compose down -v
docker-compose up -d
```

### API Key Issues

```bash
# Verify keys are set
docker-compose exec backend env | grep -E "OPENAI|AFRICAS|WEATHER"

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY" | head

# If 401, key is invalid
```

---

## Monitoring & Maintenance

### Daily Tasks

```bash
# Check service status
docker-compose ps

# View recent logs
docker-compose logs --tail 50 backend

# Monitor resources
docker stats

# Check database size
docker-compose exec postgres psql -U agri_user -d agri_chatbot \
  -c "SELECT pg_size_pretty(pg_database_size('agri_chatbot'));"
```

### Weekly Tasks

```bash
# Backup database
docker-compose exec postgres pg_dump -U agri_user agri_chatbot > backup.sql

# Update market prices
# Use admin panel or API

# Review logs for errors
docker-compose logs backend | grep ERROR
```

### Monthly Tasks

```bash
# Check for updates
docker-compose pull

# Review performance metrics
docker stats --no-stream

# Update SSL certificates (if using Let's Encrypt)
sudo certbot renew

# Check disk space
df -h
```

---

## Quick Reference: Deployment Checklist

### Pre-Deployment
- [ ] Get API keys (OpenAI, Africa's Talking, Weather)
- [ ] Choose hosting platform
- [ ] Read platform documentation
- [ ] Prepare domain name (optional)

### Deployment
- [ ] Clone/upload repository
- [ ] Configure .env file
- [ ] Start services
- [ ] Verify all services running
- [ ] Test endpoints
- [ ] Add test data

### Post-Deployment
- [ ] Configure Africa's Talking callbacks
- [ ] Add farmers to database
- [ ] Add market prices
- [ ] Setup backups
- [ ] Setup monitoring
- [ ] Configure domain (optional)

### Going Live
- [ ] Test with real SMS/USSD
- [ ] Verify all channels working
- [ ] Setup alerts
- [ ] Document procedures
- [ ] Train admin users

---

## Support & Troubleshooting

**Need help?**
1. Check logs: `docker-compose logs`
2. Review: `docs/API.md`
3. Test endpoint: `curl http://localhost:8000/health`
4. Check configuration: `docker-compose config`

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Status**: Ready for Production ✅

Choose your deployment option and follow the steps carefully. Most deployments take 30-60 minutes from start to finish!
