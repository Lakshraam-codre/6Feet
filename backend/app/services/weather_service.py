"""
Weather Service - Handles weather API calls and data caching
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import httpx
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import WeatherCache

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather data operations"""
    
    def __init__(self):
        """Initialize weather service"""
        self.provider = settings.weather_provider
        self.api_key = settings.weather_api_key
        self.cache_duration = 3600  # 1 hour in seconds
    
    async def get_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a location
        
        Args:
            location: Location name (e.g., "Maseru", "Thaba-Tseka")
            
        Returns:
            Dictionary with weather data or None if unavailable
        """
        try:
            # Check cache first
            cached = self._get_cached_weather(location)
            if cached:
                logger.info(f"Weather data from cache for {location}")
                return cached
            
            # Fetch fresh data
            if self.provider == "openweather":
                weather_data = await self._fetch_openweather(location)
            elif self.provider == "weatherapi":
                weather_data = await self._fetch_weatherapi(location)
            else:
                weather_data = await self._fetch_openweather(location)  # Default
            
            # Cache the result
            if weather_data:
                self._cache_weather(location, weather_data)
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error fetching weather for {location}: {str(e)}")
            return self._get_cached_weather(location) or self._get_fallback_weather()
    
    async def _fetch_openweather(self, location: str) -> Optional[Dict[str, Any]]:
        """Fetch weather from OpenWeather API"""
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None
        
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "location": data["name"],
                    "temperature": data["main"]["temp"],
                    "condition": data["weather"][0]["main"],
                    "humidity": data["main"]["humidity"],
                    "rainfall_mm": data.get("rain", {}).get("1h", 0),
                    "wind_speed": data["wind"]["speed"],
                }
            else:
                logger.warning(f"OpenWeather API error: {response.status_code}")
                return None
    
    async def _fetch_weatherapi(self, location: str) -> Optional[Dict[str, Any]]:
        """Fetch weather from WeatherAPI"""
        if not self.api_key:
            logger.warning("WeatherAPI key not configured")
            return None
        
        url = f"https://api.weatherapi.com/v1/current.json"
        params = {
            "key": self.api_key,
            "q": location,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "location": data["location"]["name"],
                    "temperature": data["current"]["temp_c"],
                    "condition": data["current"]["condition"]["text"],
                    "humidity": data["current"]["humidity"],
                    "rainfall_mm": data["current"].get("precip_mm", 0),
                    "wind_speed": data["current"]["wind_kph"] / 3.6,  # Convert to m/s
                }
            else:
                logger.warning(f"WeatherAPI error: {response.status_code}")
                return None
    
    def _get_cached_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get weather from cache if available and not expired"""
        try:
            db = SessionLocal()
            cache = db.query(WeatherCache).filter(
                WeatherCache.location == location,
                WeatherCache.expires_at > datetime.utcnow()
            ).first()
            db.close()
            
            if cache:
                return {
                    "location": cache.location,
                    "temperature": cache.temperature,
                    "condition": cache.condition,
                    "humidity": cache.humidity,
                    "rainfall_mm": cache.rainfall_mm,
                    "wind_speed": cache.wind_speed,
                    "cached": True,
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving cached weather: {str(e)}")
            return None
    
    def _cache_weather(self, location: str, weather_data: Dict[str, Any]) -> None:
        """Cache weather data in database"""
        try:
            db = SessionLocal()
            cache_entry = WeatherCache(
                location=location,
                temperature=weather_data["temperature"],
                condition=weather_data["condition"],
                humidity=weather_data.get("humidity"),
                rainfall_mm=weather_data.get("rainfall_mm"),
                wind_speed=weather_data.get("wind_speed"),
                cached_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(seconds=self.cache_duration)
            )
            db.add(cache_entry)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Error caching weather: {str(e)}")
    
    def _get_fallback_weather(self) -> Dict[str, Any]:
        """Get fallback weather data for Lesotho highlands"""
        return {
            "location": "Lesotho",
            "temperature": 15,  # Average highland temperature
            "condition": "Partly Cloudy",
            "humidity": 65,
            "rainfall_mm": 0,
            "wind_speed": 3.5,
            "fallback": True,
        }
    
    def get_weather_alert(self, weather_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate alert based on weather conditions
        
        Returns:
            Alert message if conditions warrant it, None otherwise
        """
        temp = weather_data.get("temperature", 20)
        condition = weather_data.get("condition", "").lower()
        
        if temp < 0:
            return "⚠️ FROST ALERT: Temperatures below freezing. Protect young plants and sensitive crops."
        elif temp > 35:
            return "⚠️ HEAT ALERT: Very hot today. Increase irrigation frequency. Water early morning/evening."
        elif "rain" in condition or weather_data.get("rainfall_mm", 0) > 10:
            return "☔ RAIN FORECAST: Good for crops. Check drainage. Watch for waterlogging."
        elif weather_data.get("humidity", 50) < 30:
            return "🌤️ DRY CONDITIONS: Low humidity. Increase watering frequency."
        
        return None
