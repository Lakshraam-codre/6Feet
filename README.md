# Agriculture Extension Chatbot - Lesotho

## Overview

This is a comprehensive Agriculture Extension Chatbot designed specifically for farmers and agricultural advisors in Lesotho. It provides real-time, localized farming guidance through multiple channels (SMS, USSD, voice, and web) to support food security and sustainable farming practices (SDG 2).

## Features

### 🌾 Core Capabilities

- **Multi-Channel Access**: SMS, USSD (basic phones), Voice IVR, and Web chat interface
- **Real-Time Localized Advice**: Crop-specific guidance based on growth stage, location, and current conditions
- **Weather Intelligence**: Location-based weather alerts, drought warnings, frost alerts
- **Market Information**: Current crop prices, demand levels, and best selling times
- **Pest & Disease Alerts**: Real-time alerts for common Lesotho pests (fall armyworm, grasshoppers, etc.)
- **Bilingual Support**: English and Sesotho
- **Low-Literacy Friendly**: Simplified instructions and voice guidance options
- **Offline Resilience**: Cached data and general best practices for low-connectivity scenarios

### 📱 Supported Channels

1. **SMS**: For farmers with basic phones
   - 160 character limit per message
   - Text-based Q&A
   - Alert delivery

2. **USSD**: For feature phones without data
   - Menu-driven interface
   - 182 character per screen
   - Fast, reliable navigation

3. **Voice**: IVR system with text-to-speech
   - Call-based guidance
   - DTMF menu navigation
   - Hands-free operation

4. **Web**: Rich interface with advanced features
   - Live chat with the chatbot
   - Weather dashboard
   - Market price lookup
   - Admin panel for data management

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Channels                        │
│  SMS  │  USSD  │  Voice  │  Web Chat  │  Admin Panel  │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│         Africa's Talking Gateway                        │
│  SMS/USSD/Voice API for routing                        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│           FastAPI Backend (Python)                      │
│  ┌─────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │ LLM Service │  │ Weather Service │  │Market Service│ │
│  │ (OpenAI)    │  │ (APIs)         │  │(Database)    │ │
│  └─────────────┘  └────────────────┘  └──────────────┘ │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│           PostgreSQL Database                           │
│  • Farmers  • Crops  • Prices  • Weather  • Logs       │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
agri-chatbot/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Configuration settings
│   │   │   ├── database.py        # Database setup
│   │   │   └── prompts.py         # System prompt & context building
│   │   ├── models/
│   │   │   └── models.py          # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py         # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── llm_service.py            # OpenAI integration
│   │   │   ├── weather_service.py        # Weather API integration
│   │   │   ├── market_service.py         # Market data management
│   │   │   └── africas_talking_service.py # SMS/USSD/Voice
│   │   ├── api/
│   │   │   ├── admin.py                  # Admin routes
│   │   │   └── channels/
│   │   │       ├── sms.py                # SMS webhook
│   │   │       ├── ussd.py               # USSD webhook
│   │   │       └── web.py                # Web chat & APIs
│   │   └── main.py                       # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatMessage.js
│   │   │   └── InputBox.js
│   │   ├── pages/
│   │   │   ├── ChatPage.js
│   │   │   ├── Dashboard.js
│   │   │   └── AdminPanel.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── ChatPage.css
│   │   │   ├── Dashboard.css
│   │   │   └── AdminPanel.css
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── docs/
│   ├── API.md          # API documentation
│   ├── DEPLOYMENT.md   # Deployment guide
│   └── SETUP.md        # Setup instructions
├── config/
│   └── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- OpenAI API key
- Africa's Talking account
- Weather API key (OpenWeather or WeatherAPI)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database URL
   ```

5. **Initialize database**:
   ```bash
   python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

6. **Run backend**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create .env file**:
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
   ```

4. **Run development server**:
   ```bash
   npm start
   ```

Frontend will be available at: `http://localhost:3000`

## API Documentation

### Web Chat Endpoint

**POST** `/api/channels/web/chat`

```json
{
  "farmer_id": 1,
  "message": "How do I prevent fall armyworm in my maize?",
  "channel": "web",
  "language": "english"
}
```

**Response**:
```json
{
  "response": "To prevent fall armyworm in maize...",
  "interaction_id": 42,
  "tokens_used": 150
}
```

### SMS Webhook

**POST** `/api/channels/sms/webhook`

Africa's Talking sends farmer SMS to this endpoint. Backend processes and responds automatically.

### Market Prices

**GET** `/api/channels/web/market/{crop_name}`

```bash
curl http://localhost:8000/api/channels/web/market/maize?location=Maseru
```

### Admin Endpoints

#### List Farmers
**GET** `/api/admin/farmers?skip=0&limit=100`

#### Add Market Price
**POST** `/api/admin/market-prices`
```json
{
  "crop_name": "maize",
  "location": "Maseru",
  "price_per_kg": 3.50,
  "demand_level": "high"
}
```

#### Send Bulk Alerts
**POST** `/api/admin/alerts/send-bulk`
```json
{
  "alert_type": "pest",
  "title": "Fall Armyworm Alert",
  "message": "Fall armyworm detected in Maseru region. Spray immediately.",
  "severity": "high"
}
```

#### Get Statistics
**GET** `/api/admin/stats`

See `docs/API.md` for complete API documentation.

## Database Schema

### farmers
- id (PK)
- phone_number (unique)
- location
- name
- language_preference (english/sesotho)
- literacy_level (basic/intermediate/advanced)
- farming_experience
- primary_crop
- farm_size_hectares
- soil_type
- created_at, last_interaction

### crop_sessions
- id (PK)
- farmer_id (FK)
- crop_name
- growth_stage
- planting_date
- expected_harvest
- current_status
- notes

### market_prices
- id (PK)
- crop_name, location
- price_per_kg
- demand_level
- best_selling_period
- last_updated

### weather_cache
- id (PK)
- location
- temperature, condition, humidity
- rainfall_mm, wind_speed
- cached_at, expires_at

### interactions
- id (PK)
- farmer_id (FK)
- channel (sms/ussd/voice/web)
- user_message, bot_response
- interaction_type
- duration_seconds, created_at

### alerts
- id (PK)
- farmer_id (FK)
- alert_type (drought/frost/pest/disease/weather/market)
- title, message, severity
- is_sent, sent_at

## Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/agri_chatbot

# LLM
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo

# Africa's Talking
AFRICAS_TALKING_API_KEY=...
AFRICAS_TALKING_USERNAME=...
SMS_SHORTCODE=lesotho_agri
USSD_CODE=*384*50234#

# Weather
WEATHER_API_KEY=...
WEATHER_PROVIDER=openweather

# Security
SECRET_KEY=change-in-production
```

## Deployment

### Using Docker

```bash
docker-compose up -d
```

### Using Railway/Render

See `docs/DEPLOYMENT.md` for cloud deployment instructions.

### Using traditional hosting

See `docs/DEPLOYMENT.md` for VPS/server deployment steps.

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Lesotho-Specific Knowledge Base

### Main Crops
- Maize
- Wheat
- Sorghum
- Beans
- Potatoes
- Cabbage

### Climate
- Highland elevation: 1,400-3,400m
- Cool temperatures year-round
- Annual rainfall: 600-800mm
- Main growing season: October-April

### Common Pests
- Fall armyworm (Spodoptera frugiperda)
- Grasshoppers
- Storage pests
- Aphids

### Soil Issues
- Acidic soils (common)
- Erosion vulnerability
- Low nitrogen availability

## Support & Troubleshooting

### Database connection issues

```bash
# Test PostgreSQL connection
psql postgresql://user:password@localhost/agri_chatbot -c "SELECT 1"
```

### LLM errors

Check that OpenAI API key is valid and has available credits.

### Weather API issues

Verify API key and rate limits with your weather provider.

### Africa's Talking SMS not working

1. Check API credentials in .env
2. Verify sandbox/production mode
3. Test with Africa's Talking dashboard

## Contributing

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Developed to support SDG 2: Zero Hunger
- Built for Lesotho's agricultural development
- Powered by OpenAI LLM
- Integrated with Africa's Talking for connectivity

## Contact

For issues, questions, or contributions, please open an issue on GitHub.

---

**Last Updated**: November 2025
**Version**: 1.0.0
