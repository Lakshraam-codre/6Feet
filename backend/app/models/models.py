"""
SQLAlchemy database models for Agriculture Extension Chatbot
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class Farmer(Base):
    """Farmer profile"""
    __tablename__ = "farmers"
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True, index=True)
    location = Column(String, nullable=True)
    name = Column(String, nullable=True)
    language_preference = Column(String, default="english")  # english, sesotho
    literacy_level = Column(String, default="basic")  # basic, intermediate, advanced
    farming_experience = Column(String, default="beginner")  # beginner, intermediate, experienced
    primary_crop = Column(String, nullable=True)
    farm_size_hectares = Column(Float, nullable=True)
    soil_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    crop_sessions = relationship("CropSession", back_populates="farmer")
    interactions = relationship("Interaction", back_populates="farmer")


class CropSession(Base):
    """Track farmer's current crop and stage"""
    __tablename__ = "crop_sessions"
    
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    crop_name = Column(String)
    growth_stage = Column(String, nullable=True)  # planting, germination, vegetative, flowering, fruit-set, maturity
    planting_date = Column(DateTime, nullable=True)
    expected_harvest = Column(DateTime, nullable=True)
    current_status = Column(String, nullable=True)  # healthy, pest_issue, drought_stress, other
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="crop_sessions")


class MarketPrice(Base):
    """Market price data for crops"""
    __tablename__ = "market_prices"
    
    id = Column(Integer, primary_key=True)
    crop_name = Column(String, index=True)
    location = Column(String)  # District: Maseru, Thaba-Tseka, etc.
    price_per_kg = Column(Float)
    currency = Column(String, default="LSL")  # Lesotho Loti
    demand_level = Column(String)  # low, medium, high
    best_selling_period = Column(String, nullable=True)  # Season when prices are best
    last_updated = Column(DateTime, default=datetime.utcnow)
    source = Column(String, nullable=True)  # Manual, API, etc.
    

class WeatherCache(Base):
    """Cached weather data"""
    __tablename__ = "weather_cache"
    
    id = Column(Integer, primary_key=True)
    location = Column(String, index=True)
    temperature = Column(Float)
    condition = Column(String)  # sunny, cloudy, rainy, etc.
    humidity = Column(Float, nullable=True)
    rainfall_mm = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    forecast_day = Column(Integer, default=0)  # 0 for today, 1 for tomorrow, etc.
    cached_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class AlertType(str, enum.Enum):
    """Types of alerts"""
    DROUGHT = "drought"
    FROST = "frost"
    PEST = "pest"
    DISEASE = "disease"
    WEATHER = "weather"
    MARKET = "market"
    OTHER = "other"


class Alert(Base):
    """Agricultural alerts and notifications"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    alert_type = Column(Enum(AlertType))
    title = Column(String)
    message = Column(Text)
    location = Column(String, nullable=True)
    severity = Column(String)  # low, medium, high, critical
    action_recommended = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    is_sent = Column(Boolean, default=False)


class Interaction(Base):
    """Log of all farmer interactions"""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    channel = Column(String)  # sms, ussd, voice, web
    user_message = Column(Text)
    bot_response = Column(Text)
    response_tokens = Column(Integer, nullable=True)
    interaction_type = Column(String)  # crop_advice, weather, market_price, pest_alert, general
    duration_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="interactions")


class PestAlert(Base):
    """Known pest and disease alerts for Lesotho"""
    __tablename__ = "pest_alerts"
    
    id = Column(Integer, primary_key=True)
    pest_name = Column(String)
    affected_crops = Column(String)  # comma-separated
    season = Column(String)  # e.g., "November-March"
    symptoms = Column(Text)
    prevention_methods = Column(Text)
    treatment_methods = Column(Text)
    severity = Column(String)  # low, medium, high, critical
    regions = Column(String)  # Affected regions
    active = Column(Boolean, default=True)
