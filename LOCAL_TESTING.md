# 🧪 Local Testing Guide

Complete instructions for testing your chatbot locally before deployment.

---

## Prerequisites Checklist

Before starting, verify you have:

- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] All API keys obtained (see GET_API_KEYS.md)
- [ ] backend/.env configured with API keys
- [ ] Python 3.11+ installed
- [ ] Node.js 14+ installed

---

## Part 1: Start All Services (10 minutes)

### Step 1: Open Terminal/PowerShell

```powershell
# Navigate to project directory
cd C:\Users\laksh\OneDrive\Desktop\googleai

# Start all services
docker-compose up -d

# Watch the logs
docker-compose logs -f
```

### Step 2: Wait for Services to Start

Expected output (wait 30 seconds):
```
[+] Running 4/4
 ✓ postgres         Started
 ✓ backend          Started
 ✓ frontend         Started
```

### Step 3: Verify All Services Running

```powershell
docker-compose ps
```

Expected output:
```
NAME        STATUS              PORTS
postgres    Up 1 minute         5432/tcp
backend     Up 30 seconds       8000/tcp
frontend    Up 30 seconds       3000/tcp
```

If any service is not "Up", check logs:
```powershell
docker-compose logs <service_name>
```

---

## Part 2: Test Backend API (15 minutes)

### Test 1: Health Check

```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Agriculture Extension Chatbot - Lesotho",
  "version": "1.0.0"
}
```

### Test 2: API Documentation

Open in browser:
```
http://localhost:8000/docs
```

You should see interactive API documentation (Swagger UI).

### Test 3: Create Test Farmer

```powershell
$body = @{
    phone_number = "+266123456789"
    location = "Maseru"
    name = "Test Farmer"
    language_preference = "english"
    literacy_level = "basic"
    farming_experience = "beginner"
    primary_crop = "maize"
    farm_size_hectares = 0.5
    soil_type = "loamy"
} | ConvertTo-Json

curl -X POST http://localhost:8000/api/admin/farmers `
  -H "Content-Type: application/json" `
  -Body $body
```

Expected response:
```json
{
  "id": 1,
  "phone_number": "+266123456789",
  "location": "Maseru",
  "name": "Test Farmer",
  ...
}
```

### Test 4: Add Market Price

```powershell
$body = @{
    crop_name = "maize"
    location = "Maseru"
    price_per_kg = 3.50
    currency = "LSL"
    demand_level = "high"
    best_selling_period = "May-July"
    source = "manual"
} | ConvertTo-Json

curl -X POST http://localhost:8000/api/admin/market-prices `
  -H "Content-Type: application/json" `
  -Body $body
```

Expected: Market price created successfully

### Test 5: Chat API

```powershell
$body = @{
    farmer_id = 1
    message = "How do I grow maize?"
    channel = "web"
    language = "english"
} | ConvertTo-Json

curl -X POST http://localhost:8000/api/channels/web/chat `
  -H "Content-Type: application/json" `
  -Body $body
```

Expected response:
```json
{
  "response": "Maize (corn) farming...",
  "tokens_used": 45,
  "duration_ms": 250
}
```

### Test 6: Get Weather

```powershell
curl http://localhost:8000/api/channels/web/weather/Maseru
```

Expected response:
```json
{
  "location": "Maseru",
  "temperature": 22,
  "condition": "Partly Cloudy",
  "humidity": 65,
  ...
}
```

### Test 7: Get Market Prices

```powershell
curl http://localhost:8000/api/channels/web/market/maize
```

Expected response:
```json
{
  "crop": "maize",
  "prices": [
    {
      "location": "Maseru",
      "price": 3.50,
      "currency": "LSL",
      ...
    }
  ]
}
```

---

## Part 3: Test Frontend (10 minutes)

### Step 1: Open Web Interface

Open browser:
```
http://localhost:3000
```

You should see:
- Chat interface with message history
- Input box for typing messages
- Admin panel button

### Step 2: Test Chat Functionality

1. In the chat interface, type: "What crops grow best in Lesotho?"
2. Press Enter
3. Wait for response from chatbot
4. You should see AI-generated response about Lesotho crops

### Step 3: Test Language Switching

1. Look for language toggle button (EN/LS)
2. Click to switch to Sesotho (LS)
3. Type a message
4. Response should attempt Sesotho (check logs for details)

### Step 4: Access Admin Panel

1. Click "Admin Panel" button
2. You should see three tabs: "Market Prices", "Alerts", "Farmers"
3. Try adding a test market price through the form

### Step 5: View Dashboard

1. Click "Dashboard" button
2. You should see statistics cards:
   - Total Farmers
   - Total Interactions
   - Alerts Sent
   - Market Prices
3. View tables below with recent data

---

## Part 4: Test Database (10 minutes)

### Connect to Database

```powershell
# Enter database container
docker-compose exec postgres psql -U agri_user -d agri_chatbot

# Now you're in PostgreSQL interactive mode
```

### Run Database Queries

```sql
-- Check farmers table
SELECT COUNT(*) as total_farmers FROM farmers;

-- Check market prices
SELECT * FROM market_prices;

-- Check recent interactions
SELECT * FROM interactions ORDER BY created_at DESC LIMIT 5;

-- Exit
\q
```

Expected: See your test data from earlier tests

---

## Part 5: Test Database Connectivity from Backend

```powershell
# Check if backend can connect to database
docker-compose exec backend python -c "
from app.core.database import SessionLocal
try:
    db = SessionLocal()
    result = db.execute('SELECT 1')
    print('✓ Database connection successful')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
"
```

---

## Part 6: View Application Logs

### Backend Logs

```powershell
# Live logs
docker-compose logs -f backend

# Last 50 lines
docker-compose logs --tail 50 backend

# With timestamps
docker-compose logs --timestamps backend
```

### Frontend Logs

```powershell
docker-compose logs -f frontend
```

### Database Logs

```powershell
docker-compose logs -f postgres
```

---

## Part 7: Comprehensive Integration Test

This test verifies end-to-end functionality:

### Create Test Scenario

```powershell
# 1. Add farmer
$farmer = curl -X POST http://localhost:8000/api/admin/farmers `
  -H "Content-Type: application/json" `
  -Body '@{phone_number="+266987654321";location="Leribe";name="Integration Farmer";language_preference="english";primary_crop="wheat"}' | ConvertTo-Json

# 2. Add market prices
curl -X POST http://localhost:8000/api/admin/market-prices `
  -H "Content-Type: application/json" `
  -Body '@{crop_name="wheat";location="Leribe";price_per_kg=4.50;demand_level="medium"}' | ConvertTo-Json

# 3. Get weather
curl http://localhost:8000/api/channels/web/weather/Leribe

# 4. Send chat message
curl -X POST http://localhost:8000/api/channels/web/chat `
  -H "Content-Type: application/json" `
  -Body '@{farmer_id=1;message="When should I plant wheat?";channel="web";language="english"}' | ConvertTo-Json

# 5. Verify in database
docker-compose exec postgres psql -U agri_user -d agri_chatbot `
  -c "SELECT COUNT(*) FROM interactions WHERE farmer_id = 1;"
```

Expected: All operations succeed, data persists in database

---

## Part 8: Performance Testing

### Load Database

Add multiple market prices to test performance:

```powershell
# Add 50 market prices for different crops/locations
$crops = @("maize", "wheat", "sorghum", "beans", "potatoes", "cabbage")
$locations = @("Maseru", "Leribe", "Berea", "Mafeteng", "Mohale's Hoek")

foreach ($crop in $crops) {
    foreach ($location in $locations) {
        $body = @{
            crop_name = $crop
            location = $location
            price_per_kg = (Get-Random -Minimum 2 -Maximum 8)
            demand_level = @("low", "medium", "high") | Get-Random
            source = "test"
        } | ConvertTo-Json
        
        curl -X POST http://localhost:8000/api/admin/market-prices `
          -H "Content-Type: application/json" `
          -Body $body
    }
}
```

### Test Response Time

```powershell
# Measure chat response time
Measure-Command {
    curl -X POST http://localhost:8000/api/channels/web/chat `
      -H "Content-Type: application/json" `
      -Body '@{farmer_id=1;message="Tell me about pest management";channel="web"}' | Out-Null
} | Select-Object TotalMilliseconds
```

Expected: Response under 1000ms

---

## Part 9: Error Testing

### Test API Error Handling

```powershell
# Invalid farmer ID
curl http://localhost:8000/api/channels/web/weather/InvalidLocation

# Missing required field
curl -X POST http://localhost:8000/api/channels/web/chat `
  -H "Content-Type: application/json" `
  -Body '@{farmer_id=1;message="test"}' 

# Database error recovery
docker-compose restart postgres
# Try API call - should handle gracefully
```

---

## Part 10: Cleanup & Stop

### Stop All Services

```powershell
# Stop services (keep data)
docker-compose down

# Stop and remove everything
docker-compose down -v
```

### View Resource Usage

```powershell
# See current usage
docker stats

# View images
docker images

# View volumes
docker volume ls
```

---

## Troubleshooting Test Issues

### Backend Won't Start

```powershell
# Check logs
docker-compose logs backend

# Restart
docker-compose restart backend

# If still failing, rebuild
docker-compose up --build backend
```

### Frontend Blank

```powershell
# Check if API URL is correct
docker-compose exec frontend cat .env

# Rebuild frontend
docker-compose up --build frontend
```

### Database Connection Failed

```powershell
# Wait longer (database needs 30 seconds)
timeout /t 30

# Check database logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
timeout /t 30
docker-compose up -d
```

### Chat Responses Not Working

```powershell
# Check if OpenAI key is valid
docker-compose exec backend python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'Key length: {len(key)}')
print(f'Key starts with: {key[:10]}...')
"

# Test OpenAI connection
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.openai.com/v1/models | head
```

---

## Test Results Checklist

After completing all tests, verify:

- [ ] Backend health check returns 200 OK
- [ ] API documentation loads at /docs
- [ ] Can create farmer via API
- [ ] Can add market prices via API
- [ ] Weather API returns data
- [ ] Chat sends and receives messages
- [ ] Frontend loads without errors
- [ ] Admin panel forms work
- [ ] Dashboard displays stats
- [ ] Database queries return data
- [ ] Logs show no critical errors

---

## Success!

If all tests pass, your application is ready for:
1. **Local development** - make changes and test
2. **Demo to stakeholders** - show working system
3. **Production deployment** - follow DEPLOYMENT_STEPS.md

---

**Estimated Total Time**: 45-60 minutes
**Difficulty**: Medium
**Status**: Essential before deployment ✓

---

## Next Steps

After successful testing:
1. ✅ Local testing complete → Ready for deployment
2. Choose deployment platform (DEPLOYMENT_STEPS.md)
3. Configure Africa's Talking for SMS/USSD
4. Deploy to production
5. Go live with your chatbot!

