# Setup Guide

## Complete Setup Instructions

This guide will walk you through setting up the Agriculture Extension Chatbot for Lesotho.

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **CPU**: 2+ cores
- **RAM**: 4GB minimum
- **Disk**: 10GB free space
- **Internet**: Stable connection for API calls

### Software Requirements
- Git
- Docker & Docker Compose (recommended) OR
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+ (if not using Docker)

### API Keys Required
1. **OpenAI**: https://platform.openai.com/api-keys
2. **Africa's Talking**: https://africastalking.com
3. **Weather API**: https://openweathermap.org or https://weatherapi.com (free tier available)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agri-chatbot.git
cd agri-chatbot
```

## Step 2: Setup Backend

### Option A: Using Docker (Recommended)

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit with your API keys
nano backend/.env
```

Fill in the following in `.env`:
```env
# Required - Get from OpenAI dashboard
OPENAI_API_KEY=sk-your_key_here

# Required - Get from Africa's Talking
AFRICAS_TALKING_API_KEY=your_key
AFRICAS_TALKING_USERNAME=your_username

# Required - Get from weather provider
WEATHER_API_KEY=your_key
```

### Option B: Manual Setup (Python Virtual Environment)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Add your API keys

# Create database (requires PostgreSQL running)
# Update DATABASE_URL in .env first

# Create tables
python3 -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

## Step 3: Setup Frontend

### Option A: Using Docker

Frontend will be built and run by Docker Compose.

### Option B: Manual Setup (Node.js)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Start development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## Step 4: Setup Database

### Option A: Using Docker

Docker Compose handles database setup automatically.

### Option B: Manual PostgreSQL Setup

```bash
# Create database
createdb -U postgres agri_chatbot

# Connect and create user
psql -U postgres -d agri_chatbot -c "CREATE USER agri_user WITH PASSWORD 'agri_password';"
psql -U postgres -d agri_chatbot -c "GRANT ALL PRIVILEGES ON DATABASE agri_chatbot TO agri_user;"

# Update DATABASE_URL in backend/.env:
DATABASE_URL=postgresql://agri_user:agri_password@localhost/agri_chatbot
```

## Step 5: Run Application

### Option A: Using Docker Compose (Recommended)

```bash
cd agri-chatbot

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

All services will start:
- PostgreSQL on `localhost:5432`
- Backend on `localhost:8000`
- Frontend on `localhost:3000`

### Option B: Manual Setup

Terminal 1 - PostgreSQL (if not using Docker):
```bash
# Make sure PostgreSQL service is running
# On Linux: sudo systemctl start postgresql
# On macOS: brew services start postgresql
```

Terminal 2 - Backend:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 3 - Frontend:
```bash
cd frontend
npm start
```

## Step 6: Verify Installation

### Check Backend

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "service": "Agriculture Extension Chatbot - Lesotho",
  "version": "1.0.0"
}
```

### Check Frontend

Open `http://localhost:3000` in your browser.

### Check Database

```bash
# Using Docker
docker-compose exec postgres psql -U agri_user -d agri_chatbot -c "SELECT version();"

# Or manually
psql -U agri_user -d agri_chatbot -c "SELECT version();"
```

## Step 7: Create Initial Data

### Add Test Farmer

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
```

### Add Sample Market Prices

```bash
curl -X POST http://localhost:8000/api/admin/market-prices \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "maize",
    "location": "Maseru",
    "price_per_kg": 3.50,
    "demand_level": "high",
    "best_selling_period": "May-July"
  }'
```

## Step 8: Configure Africa's Talking (SMS/USSD)

1. **Get credentials**: https://africastalking.com
2. **In Africa's Talking Dashboard**:
   - Obtain API key and username
   - Configure SMS shortcode (e.g., lesotho_agri)
   - Configure USSD code (e.g., *384*50234#)
   - Set callback URL to: `https://yourdomain.com/api/channels/sms/webhook`

3. **Update backend/.env**:
   ```env
   AFRICAS_TALKING_API_KEY=your_api_key
   AFRICAS_TALKING_USERNAME=your_username
   SMS_SHORTCODE=lesotho_agri
   USSD_CODE=*384*50234#
   ```

4. **Test SMS**: Send SMS to the shortcode from any phone

## Step 9: Configure Weather API

### OpenWeather (Recommended)

1. Go to https://openweathermap.org/api
2. Sign up and get free API key
3. Update `.env`:
   ```env
   WEATHER_API_KEY=your_openweather_key
   WEATHER_PROVIDER=openweather
   ```

### WeatherAPI

1. Go to https://www.weatherapi.com
2. Get free API key
3. Update `.env`:
   ```env
   WEATHER_API_KEY=your_weatherapi_key
   WEATHER_PROVIDER=weatherapi
   ```

## Step 10: Test Chat

### Via Web Interface

1. Open `http://localhost:3000`
2. Type a question: "How do I grow maize?"
3. Should receive response from chatbot

### Via API

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

## Troubleshooting

### Port Already in Use

```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml or uvicorn command
```

### Database Connection Error

```bash
# Check database is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### API Key Issues

- Verify API keys in `.env`
- Check API key permissions/quotas
- For OpenAI: https://platform.openai.com/account/billing/overview
- For Africa's Talking: Check account balance and sandbox mode

### Frontend Not Loading

```bash
# Check if frontend service is running
docker-compose ps frontend

# View logs
docker-compose logs frontend

# Verify API URL is correct
echo $REACT_APP_API_URL

# Clear Node cache and rebuild
docker-compose down
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### LLM Not Responding

- Verify OpenAI API key is valid
- Check API rate limits
- See backend logs: `docker-compose logs backend`
- Fallback responses will be used if LLM unavailable

## Next Steps

1. **Deploy**: See `docs/DEPLOYMENT.md`
2. **Integrate Africa's Talking**: Follow setup in Step 8
3. **Add Market Data**: Use admin panel or API
4. **Customize System Prompt**: Edit `backend/app/core/prompts.py`
5. **Scale Up**: Add more farmers and test at scale
6. **Monitor**: Setup monitoring and alerts

## Support

- **Documentation**: See `README.md` and `docs/` folder
- **API Reference**: See `docs/API.md`
- **Issues**: Open GitHub issue or check logs
- **Logs**:
  ```bash
  docker-compose logs backend
  docker-compose logs frontend
  docker-compose logs postgres
  ```

## Security Checklist

- [ ] Changed default passwords
- [ ] Set strong SECRET_KEY
- [ ] API keys not committed to Git
- [ ] Using HTTPS in production
- [ ] CORS properly configured
- [ ] Database backups enabled
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Environment variables secured

---

**Congratulations!** Your Agriculture Extension Chatbot is now running.

For production deployment, see `docs/DEPLOYMENT.md`

**Last Updated**: November 2025
