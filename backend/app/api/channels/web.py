"""
Web Chat Channel - Web-based chat interface
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Farmer, Interaction
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.services.weather_service import WeatherService
from app.services.market_service import MarketService
from datetime import datetime
import time

router = APIRouter(prefix="/api/channels/web", tags=["Web Chat"])
llm_service = LLMService()
weather_service = WeatherService()
logger = logging.getLogger(__name__)


@router.post("/chat")
async def web_chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """
    Handle web chat messages
    
    Args:
        request: ChatRequest with message and farmer details
        
    Returns:
        ChatResponse with bot response
    """
    try:
        start_time = time.time()
        
        # Get or create farmer
        if request.farmer_id:
            farmer = db.query(Farmer).filter(Farmer.id == request.farmer_id).first()
            if not farmer:
                raise HTTPException(status_code=404, detail="Farmer not found")
        elif request.phone_number:
            farmer = db.query(Farmer).filter(Farmer.phone_number == request.phone_number).first()
            if not farmer:
                farmer = Farmer(
                    phone_number=request.phone_number,
                    language_preference=request.language,
                    literacy_level="intermediate"  # Assume intermediate for web users
                )
                db.add(farmer)
                db.commit()
        else:
            raise HTTPException(status_code=400, detail="farmer_id or phone_number required")
        
        farmer.last_interaction = datetime.utcnow()
        db.commit()
        
        # Gather context
        weather_data = None
        if farmer.location:
            weather_data = await weather_service.get_weather(farmer.location)
        
        market_data = None
        if farmer.primary_crop:
            market_price = MarketService.get_market_price(
                db, farmer.primary_crop, farmer.location
            )
            if market_price:
                market_data = market_price.dict()
        
        # Generate response
        response_text, tokens = llm_service.generate_response(
            user_message=request.message,
            channel=request.channel,
            language=request.language,
            farmer_context={
                "location": farmer.location,
                "crop": farmer.primary_crop,
                "experience_level": farmer.farming_experience,
            },
            weather_data=weather_data,
            market_data=market_data,
        )
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log interaction
        interaction = Interaction(
            farmer_id=farmer.id,
            channel=request.channel,
            user_message=request.message,
            bot_response=response_text,
            response_tokens=tokens,
            interaction_type="general",
            duration_seconds=duration
        )
        db.add(interaction)
        db.commit()
        
        logger.info(f"Web chat handled for farmer {farmer.id}, duration: {duration:.2f}s")
        
        return ChatResponse(
            response=response_text,
            interaction_id=interaction.id,
            tokens_used=tokens
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in web chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weather/{location}")
async def get_weather_alert(location: str):
    """Get current weather and alerts for a location"""
    try:
        weather_data = await weather_service.get_weather(location)
        alert = weather_service.get_weather_alert(weather_data) if weather_data else None
        
        return {
            "location": location,
            "weather": weather_data,
            "alert": alert
        }
    except Exception as e:
        logger.error(f"Error getting weather: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/{crop_name}")
async def get_market_info(crop_name: str, location: str = None, db: Session = Depends(get_db)):
    """Get market prices for a crop"""
    try:
        price = MarketService.get_market_price(db, crop_name, location)
        best_time = MarketService.get_best_selling_time(crop_name)
        
        if price:
            return {
                "crop": crop_name,
                "price": price.dict(),
                "best_selling_time": best_time
            }
        else:
            return {
                "crop": crop_name,
                "price": None,
                "best_selling_time": best_time,
                "message": f"No recent prices for {crop_name}. Check back later."
            }
            
    except Exception as e:
        logger.error(f"Error getting market info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
