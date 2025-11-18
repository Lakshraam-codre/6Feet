"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FarmerBase(BaseModel):
    """Base farmer schema"""
    phone_number: str
    location: Optional[str] = None
    name: Optional[str] = None
    language_preference: str = "english"
    literacy_level: str = "basic"
    farming_experience: str = "beginner"
    primary_crop: Optional[str] = None
    farm_size_hectares: Optional[float] = None
    soil_type: Optional[str] = None


class FarmerCreate(FarmerBase):
    """Schema for creating farmer"""
    pass


class FarmerUpdate(BaseModel):
    """Schema for updating farmer"""
    location: Optional[str] = None
    language_preference: Optional[str] = None
    literacy_level: Optional[str] = None
    farming_experience: Optional[str] = None
    primary_crop: Optional[str] = None
    farm_size_hectares: Optional[float] = None
    soil_type: Optional[str] = None


class FarmerResponse(FarmerBase):
    """Schema for farmer response"""
    id: int
    created_at: datetime
    last_interaction: datetime
    
    class Config:
        from_attributes = True


class CropSessionBase(BaseModel):
    """Base crop session schema"""
    crop_name: str
    growth_stage: Optional[str] = None
    planting_date: Optional[datetime] = None
    expected_harvest: Optional[datetime] = None
    current_status: Optional[str] = None
    notes: Optional[str] = None


class CropSessionCreate(CropSessionBase):
    """Schema for creating crop session"""
    farmer_id: int


class CropSessionResponse(CropSessionBase):
    """Schema for crop session response"""
    id: int
    farmer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MarketPriceBase(BaseModel):
    """Base market price schema"""
    crop_name: str
    location: str
    price_per_kg: float
    currency: str = "LSL"
    demand_level: str
    best_selling_period: Optional[str] = None
    source: Optional[str] = None


class MarketPriceCreate(MarketPriceBase):
    """Schema for creating market price"""
    pass


class MarketPriceResponse(MarketPriceBase):
    """Schema for market price response"""
    id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True


class WeatherCacheBase(BaseModel):
    """Base weather cache schema"""
    location: str
    temperature: float
    condition: str
    humidity: Optional[float] = None
    rainfall_mm: Optional[float] = None
    wind_speed: Optional[float] = None
    forecast_day: int = 0


class WeatherCacheResponse(WeatherCacheBase):
    """Schema for weather cache response"""
    id: int
    cached_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat/message request"""
    farmer_id: Optional[int] = None
    phone_number: Optional[str] = None
    message: str
    channel: str = "web"  # web, sms, ussd, voice
    language: str = "english"


class ChatResponse(BaseModel):
    """Schema for chat response"""
    response: str
    interaction_id: int
    tokens_used: Optional[int] = None


class SMSRequest(BaseModel):
    """Schema for SMS webhook from Africa's Talking"""
    phoneNumber: str
    text: str
    linkId: Optional[str] = None
    date: str
    id: str


class USSDRequest(BaseModel):
    """Schema for USSD webhook from Africa's Talking"""
    phoneNumber: str
    text: str
    sessionId: str
    serviceCode: str


class VoiceRequest(BaseModel):
    """Schema for Voice callback from Africa's Talking"""
    callSid: str
    phoneNumber: str
    direction: str
    duration: int
    dateCreated: str


class AlertBase(BaseModel):
    """Base alert schema"""
    alert_type: str
    title: str
    message: str
    location: Optional[str] = None
    severity: str
    action_recommended: Optional[str] = None


class AlertCreate(AlertBase):
    """Schema for creating alert"""
    farmer_id: Optional[int] = None


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    created_at: datetime
    is_sent: bool
    
    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    """Base interaction schema"""
    channel: str
    user_message: str
    bot_response: str
    interaction_type: str
    duration_seconds: Optional[float] = None


class InteractionResponse(InteractionBase):
    """Schema for interaction response"""
    id: int
    farmer_id: int
    response_tokens: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
