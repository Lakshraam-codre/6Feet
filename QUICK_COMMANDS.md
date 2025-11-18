# Quick Commands Reference

## 🚀 Getting Started

### Start Application
```bash
# Using quick start script (easiest)
./start.sh              # Linux/macOS
start.bat               # Windows

# Using Docker Compose directly
docker-compose up -d

# Manual backend start
cd backend
uvicorn app.main:app --reload

# Manual frontend start (new terminal)
cd frontend
npm start
```

### Access Application
```
Frontend:     http://localhost:3000
Backend:      http://localhost:8000
API Docs:     http://localhost:8000/docs
Database:     localhost:5432
```

## 🔧 Useful Commands

### Docker Operations
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs
docker-compose logs -f              # All logs
docker-compose logs -f backend      # Backend logs
docker-compose logs -f frontend     # Frontend logs
docker-compose logs -f postgres     # Database logs

# Rebuild services
docker-compose build --no-cache

# Run commands in container
docker-compose exec backend bash
docker-compose exec frontend bash
docker-compose exec postgres psql -U agri_user -d agri_chatbot
```

### Database Operations
```bash
# Connect to database
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# Backup database
docker-compose exec postgres pg_dump -U agri_user agri_chatbot > backup.sql

# Restore database
docker-compose exec -T postgres psql -U agri_user agri_chatbot < backup.sql

# View tables
\dt

# Check database size
SELECT pg_size_pretty(pg_database.datlen)
FROM pg_database
WHERE datname = 'agri_chatbot';
```

### Backend Management
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests
pytest

# Create database
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# View API documentation
curl http://localhost:8000/docs
```

### Frontend Management
```bash
# Install dependencies
cd frontend
npm install

# Build production
npm run build

# Run tests
npm test

# Clean cache
rm -rf node_modules package-lock.json
npm install
```

## 📝 Configuration

### Environment Setup
```bash
# Copy template
cp backend/.env.example backend/.env

# Edit with your keys
nano backend/.env
cat backend/.env  # View configuration
```

### Key Environment Variables
```env
DATABASE_URL=postgresql://agri_user:agri_password@postgres:5432/agri_chatbot
OPENAI_API_KEY=sk-...
AFRICAS_TALKING_API_KEY=...
AFRICAS_TALKING_USERNAME=...
WEATHER_API_KEY=...
DEBUG=False
```

## 🧪 Testing

### API Testing
```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/channels/web/chat \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": 1,
    "message": "How do I grow maize?",
    "channel": "web",
    "language": "english"
  }'

# Get weather
curl http://localhost:8000/api/channels/web/weather/Maseru

# Get market price
curl http://localhost:8000/api/channels/web/market/maize

# List farmers
curl http://localhost:8000/api/admin/farmers

# Get system stats
curl http://localhost:8000/api/admin/stats

# Health check
curl http://localhost:8000/health
```

## 📊 Monitoring

### Check Service Status
```bash
# View running containers
docker-compose ps

# Check logs for errors
docker-compose logs | grep ERROR
docker-compose logs | grep WARNING

# Monitor resource usage
docker stats

# View container details
docker-compose exec backend env
docker-compose exec frontend env
```

### Database Health Check
```bash
# Connect and check tables
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# Count records
SELECT COUNT(*) FROM farmers;
SELECT COUNT(*) FROM interactions;
SELECT COUNT(*) FROM market_prices;

# View recent interactions
SELECT * FROM interactions ORDER BY created_at DESC LIMIT 10;

# Check database size
SELECT * FROM pg_database_size_pretty('agri_chatbot');
```

## 🔍 Troubleshooting

### Port Issues
```bash
# Check if port is in use
lsof -i :8000              # Check port 8000
lsof -i :3000              # Check port 3000
lsof -i :5432              # Check port 5432

# Kill process on port
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Use different port
uvicorn app.main:app --port 8001
npm start -- --port 3001
```

### Connection Issues
```bash
# Test database connection
docker-compose exec postgres psql -U agri_user -d agri_chatbot -c "SELECT 1;"

# Test backend connectivity
curl -v http://localhost:8000/health

# Check network
docker-compose exec backend ping postgres
docker-compose exec frontend ping backend

# View container logs for errors
docker-compose logs backend 2>&1 | head -50
```

### Clean Up
```bash
# Remove all containers
docker-compose down

# Remove volumes (database data)
docker-compose down -v

# Clean up unused Docker resources
docker system prune -a

# Remove node_modules
rm -rf frontend/node_modules
npm install --prefix frontend

# Remove Python cache
find backend -type d -name __pycache__ -exec rm -rf {} +
```

## 📚 Documentation Quick Links

```bash
# View files
cat README.md               # Main overview
cat WELCOME.txt            # Welcome message
cat INDEX.md               # File structure
cat PROJECT_SUMMARY.md     # Technical details
cat REQUIREMENTS_CHECKLIST.md  # Status

# View documentation
cat docs/SETUP.md          # Setup guide
cat docs/API.md            # API reference
cat docs/DEPLOYMENT.md     # Deployment guide
```

## 🚀 Deployment Quick Start

### Using Railway
```bash
# Login to Railway
railway login

# Create new project
railway init

# Deploy
railway up

# View logs
railway logs
```

### Using Render
```bash
# Create blueprint.yaml in repo
# Push to GitHub
# Connect to Render
# Select repository
# Deploy
```

### Using AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@instance_ip

# Clone and setup
git clone <repo>
cd agri-chatbot

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start application
sudo docker-compose up -d
```

## 📦 Backup and Restore

### Database Backup
```bash
# Full backup
docker-compose exec postgres pg_dump -U agri_user agri_chatbot > backup_$(date +%Y%m%d).sql

# Scheduled backup (cron job)
0 2 * * * cd /path/to/agri-chatbot && docker-compose exec -T postgres pg_dump -U agri_user agri_chatbot > backup_$(date +\%Y\%m\%d).sql
```

### Database Restore
```bash
# Restore from backup
docker-compose exec -T postgres psql -U agri_user agri_chatbot < backup_20251118.sql

# Partial restore
docker-compose exec -T postgres psql -U agri_user agri_chatbot < partial_backup.sql
```

## 🔐 Security

### Check for Secrets in Code
```bash
# Search for sensitive data
grep -r "OPENAI_API_KEY" . --exclude-dir=.git
grep -r "sk-" . --exclude-dir=.git
grep -r "password" . --exclude-dir=.git

# Use git-secrets (optional)
git secrets --install
git secrets --register-aws
```

### Rotate Credentials
```bash
# Update .env with new keys
nano backend/.env

# Restart services to apply
docker-compose restart backend
```

## 📊 Performance Monitoring

### Check Backend Performance
```bash
# View request logs
docker-compose logs backend | grep "GET \|POST \|PUT \|DELETE"

# Count requests
docker-compose logs backend | wc -l

# Find slow requests
docker-compose logs backend | grep "ms"
```

### Check Database Performance
```bash
# List connections
docker-compose exec postgres psql -U agri_user -d agri_chatbot -c "SELECT * FROM pg_stat_activity;"

# Check slow queries (if enabled)
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC;

# Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 🎯 Quick Development Workflow

### Feature Development
```bash
# 1. Start containers
docker-compose up -d

# 2. Watch logs
docker-compose logs -f backend &

# 3. Edit code
nano backend/app/api/admin.py

# 4. Backend auto-reloads (uvicorn --reload)

# 5. Test changes
curl http://localhost:8000/api/admin/stats

# 6. Check frontend
# Open http://localhost:3000
```

### Bug Fixing
```bash
# 1. Check logs for errors
docker-compose logs backend | tail -50

# 2. Enable debug mode
# Edit backend/.env: DEBUG=True

# 3. Restart backend
docker-compose restart backend

# 4. Test with verbose output
curl -v http://localhost:8000/health
```

## 📞 Common Issues & Solutions

```bash
# Issue: "Address already in use"
# Solution: Kill existing process
lsof -ti:8000 | xargs kill -9

# Issue: "Connection refused"
# Solution: Check service is running
docker-compose ps

# Issue: "ModuleNotFoundError"
# Solution: Install requirements
pip install -r requirements.txt

# Issue: "No such table"
# Solution: Create tables
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Issue: API key not working
# Solution: Verify in .env file
cat backend/.env | grep KEY

# Issue: Frontend blank/error
# Solution: Check API URL
docker-compose exec frontend cat .env
```

## 📝 Log Levels

```bash
# View specific log level
docker-compose logs backend | grep ERROR
docker-compose logs backend | grep WARNING
docker-compose logs backend | grep INFO
docker-compose logs backend | grep DEBUG

# Follow specific errors
docker-compose logs -f backend | grep -E "(ERROR|Exception)"

# Search across all logs
docker-compose logs | grep "pattern"
```

---

**Last Updated**: November 2025
**Version**: 1.0.0

Print this document or bookmark it for quick reference during development!
