"""
Core configuration for Agriculture Extension Chatbot
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://user:password@localhost/agri_chatbot"
    
    # FastAPI
    app_name: str = "Agriculture Extension Chatbot - Lesotho"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    llm_model: str = "gpt-3.5-turbo"
    
    # Africa's Talking
    africas_talking_api_key: Optional[str] = None
    africas_talking_username: Optional[str] = None
    sms_shortcode: str = "lesotho_agri"
    ussd_code: str = "*384*50234#"
    voice_number: Optional[str] = None
    
    # Weather API
    weather_api_key: Optional[str] = None
    weather_provider: str = "openweather"  # openweather, tomorrow, weatherapi
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    

settings = Settings()
