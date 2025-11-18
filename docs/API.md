# Complete API Documentation

## Base URL

Production: `https://agri-chatbot.example.com/api`
Development: `http://localhost:8000/api`

## Authentication

Currently no authentication is implemented. For production, add:
- API Key authentication
- JWT tokens for admin panel
- Rate limiting per phone number

## Endpoints

### Chat Channels

#### Web Chat
**POST** `/channels/web/chat`

Send a message and get response from the chatbot.

Request:
```json
{
  "farmer_id": 1,
  "phone_number": null,
  "message": "How do I grow maize?",
  "channel": "web",
  "language": "english"
}
```

Response (200 OK):
```json
{
  "response": "To grow maize effectively in Lesotho...",
  "interaction_id": 42,
  "tokens_used": 156
}
```

Query Parameters:
- None

---

#### Get Weather
**GET** `/channels/web/weather/{location}`

Get current weather and alerts for a location.

Example: `GET /channels/web/weather/Maseru`

Response (200 OK):
```json
{
  "location": "Maseru",
  "weather": {
    "location": "Maseru",
    "temperature": 18.5,
    "condition": "Sunny",
    "humidity": 65,
    "rainfall_mm": 0,
    "wind_speed": 3.2,
    "cached": false
  },
  "alert": null
}
```

Possible alerts:
- Frost warning (temp < 0°C)
- Heat alert (temp > 35°C)
- Heavy rain forecast
- Dry conditions (humidity < 30%)

---

#### Get Market Price
**GET** `/channels/web/market/{crop_name}`

Get current market prices for a crop.

Example: `GET /channels/web/market/maize?location=Maseru`

Response (200 OK):
```json
{
  "crop": "maize",
  "price": {
    "id": 1,
    "crop_name": "maize",
    "location": "Maseru",
    "price_per_kg": 3.50,
    "currency": "LSL",
    "demand_level": "high",
    "best_selling_period": "May-July",
    "last_updated": "2025-11-18T10:30:00Z"
  },
  "best_selling_time": "May-July (after harvest)"
}
```

---

### Admin Endpoints

#### List Farmers
**GET** `/admin/farmers`

Get list of all registered farmers.

Query Parameters:
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

Response (200 OK):
```json
[
  {
    "id": 1,
    "phone_number": "+266123456789",
    "location": "Maseru",
    "name": "Ntate Ramodibedi",
    "language_preference": "english",
    "literacy_level": "basic",
    "farming_experience": "beginner",
    "primary_crop": "maize",
    "farm_size_hectares": 0.5,
    "soil_type": "loamy",
    "created_at": "2025-11-15T08:00:00Z",
    "last_interaction": "2025-11-18T10:30:00Z"
  }
]
```

---

#### Get Farmer Details
**GET** `/admin/farmers/{farmer_id}`

Get details of a specific farmer.

Response (200 OK):
```json
{
  "id": 1,
  "phone_number": "+266123456789",
  "location": "Maseru",
  "name": "Ntate Ramodibedi",
  "language_preference": "english",
  "literacy_level": "basic",
  "farming_experience": "beginner",
  "primary_crop": "maize",
  "farm_size_hectares": 0.5,
  "soil_type": "loamy",
  "created_at": "2025-11-15T08:00:00Z",
  "last_interaction": "2025-11-18T10:30:00Z"
}
```

Response (404 Not Found):
```json
{
  "detail": "Farmer not found"
}
```

---

#### Create Farmer
**POST** `/admin/farmers`

Register a new farmer.

Request:
```json
{
  "phone_number": "+266123456789",
  "location": "Maseru",
  "name": "Ntate Ramodibedi",
  "language_preference": "english",
  "literacy_level": "basic",
  "farming_experience": "beginner",
  "primary_crop": "maize",
  "farm_size_hectares": 0.5,
  "soil_type": "loamy"
}
```

Response (200 OK):
```json
{
  "id": 1,
  "phone_number": "+266123456789",
  "location": "Maseru",
  "name": "Ntate Ramodibedi",
  "language_preference": "english",
  "literacy_level": "basic",
  "farming_experience": "beginner",
  "primary_crop": "maize",
  "farm_size_hectares": 0.5,
  "soil_type": "loamy",
  "created_at": "2025-11-18T10:30:00Z",
  "last_interaction": "2025-11-18T10:30:00Z"
}
```

---

#### Update Farmer
**PUT** `/admin/farmers/{farmer_id}`

Update farmer profile.

Request (only fields to update):
```json
{
  "location": "Thaba-Tseka",
  "primary_crop": "wheat"
}
```

Response (200 OK): Updated farmer object

---

#### List Market Prices
**GET** `/admin/market-prices`

Get all market prices with optional filters.

Query Parameters:
- `crop` (string): Filter by crop name
- `location` (string): Filter by location

Response (200 OK):
```json
[
  {
    "id": 1,
    "crop_name": "maize",
    "location": "Maseru",
    "price_per_kg": 3.50,
    "currency": "LSL",
    "demand_level": "high",
    "best_selling_period": "May-July",
    "last_updated": "2025-11-18T10:30:00Z"
  }
]
```

---

#### Create/Update Market Price
**POST** `/admin/market-prices`

Add or update market price for a crop.

Request:
```json
{
  "crop_name": "maize",
  "location": "Maseru",
  "price_per_kg": 3.50,
  "currency": "LSL",
  "demand_level": "high",
  "best_selling_period": "May-July",
  "source": "manual"
}
```

Response (200 OK):
```json
{
  "id": 1,
  "crop_name": "maize",
  "location": "Maseru",
  "price_per_kg": 3.50,
  "currency": "LSL",
  "demand_level": "high",
  "best_selling_period": "May-July",
  "last_updated": "2025-11-18T10:30:00Z"
}
```

---

#### Delete Market Price
**DELETE** `/admin/market-prices/{price_id}`

Remove a market price entry.

Response (200 OK):
```json
{
  "status": "deleted"
}
```

---

#### Create Alert
**POST** `/admin/alerts`

Create a new alert.

Request:
```json
{
  "farmer_id": 1,
  "alert_type": "pest",
  "title": "Fall Armyworm Warning",
  "message": "Fall armyworm detected in Maseru. Use approved pesticides.",
  "location": "Maseru",
  "severity": "high",
  "action_recommended": "Spray all maize fields with organic pesticide."
}
```

Response (200 OK):
```json
{
  "id": 1,
  "alert_type": "pest",
  "title": "Fall Armyworm Warning",
  "message": "Fall armyworm detected in Maseru. Use approved pesticides.",
  "severity": "high",
  "created_at": "2025-11-18T10:30:00Z",
  "is_sent": false
}
```

---

#### Send Bulk Alerts
**POST** `/admin/alerts/send-bulk`

Send alert to multiple farmers via SMS.

Query Parameters:
- `location_filter` (string): Only send to farmers in this location

Request:
```json
{
  "alert_type": "pest",
  "title": "Fall Armyworm Alert",
  "message": "Fall armyworm detected in your region. Spray immediately.",
  "severity": "high"
}
```

Response (200 OK):
```json
{
  "total_farmers": 150,
  "successfully_sent": 145,
  "failed": 5
}
```

---

#### Get Statistics
**GET** `/admin/stats`

Get system statistics.

Response (200 OK):
```json
{
  "total_farmers": 250,
  "total_interactions": 1450,
  "total_alerts_sent": 85,
  "market_prices": 42
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently not implemented. Recommended for production:
- 10 requests/minute per phone number (SMS)
- 100 requests/minute per IP (web)
- 1000 requests/hour per API key (admin)

## Webhooks

### SMS Webhook

Africa's Talking sends inbound SMS to:
`POST /api/channels/sms/webhook`

Form data:
- `phoneNumber`: Sender's phone
- `text`: Message content
- `linkId`: Message ID
- `date`: Timestamp
- `id`: Africa's Talking ID

Response: JSON with status and response sent to farmer

---

## Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {},
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "status": "error",
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

---

## Testing Endpoints

### Using cURL

```bash
# Test web chat
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
curl http://localhost:8000/api/channels/web/market/maize?location=Maseru

# List farmers
curl http://localhost:8000/api/admin/farmers?limit=10

# Get stats
curl http://localhost:8000/api/admin/stats
```

---

**Last Updated**: November 2025
