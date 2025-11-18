"""
USSD Channel - Africa's Talking USSD webhook endpoints
"""
import logging
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Farmer, Interaction
from app.schemas.schemas import USSDRequest
from app.services.llm_service import LLMService
from app.services.africas_talking_service import AfricasTalkingService
from datetime import datetime

router = APIRouter(prefix="/api/channels/ussd", tags=["USSD"])
llm_service = LLMService()
at_service = AfricasTalkingService()
logger = logging.getLogger(__name__)


# Simple USSD session storage (in production, use cache like Redis)
ussd_sessions = {}


@router.post("/webhook")
async def ussd_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook to receive USSD from Africa's Talking
    
    Expects form data:
    - phoneNumber: Sender's phone number
    - text: User input (menu option or message)
    - sessionId: USSD session ID
    - serviceCode: Service code
    """
    try:
        form_data = await request.form()
        
        phone_number = form_data.get("phoneNumber", "")
        user_input = form_data.get("text", "")
        session_id = form_data.get("sessionId", "")
        
        if not phone_number:
            return "END Invalid request\n"
        
        logger.info(f"USSD from {phone_number}: {user_input}")
        
        # Get or create farmer
        farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()
        if not farmer:
            farmer = Farmer(
                phone_number=phone_number,
                language_preference="english",
                literacy_level="basic"
            )
            db.add(farmer)
            db.commit()
        
        farmer.last_interaction = datetime.utcnow()
        db.commit()
        
        # Handle USSD menu navigation
        if user_input == "":
            # Initial menu
            menu_response = _build_main_menu()
            response = f"CON {menu_response}"
            
        elif user_input == "1":
            # Crop Advice
            menu_response = _build_crop_menu()
            response = f"CON {menu_response}"
            
        elif user_input == "2":
            # Weather
            weather_text = "Weather alerts coming soon.\nReply 0 for menu."
            response = f"CON {weather_text}"
            
        elif user_input == "3":
            # Market Prices
            market_text = "Market prices coming soon.\nReply 0 for menu."
            response = f"CON {market_text}"
            
        elif user_input == "0":
            # Back to main menu
            menu_response = _build_main_menu()
            response = f"CON {menu_response}"
            
        else:
            # Process user message as crop question
            response_text, tokens = llm_service.generate_response(
                user_message=user_input,
                channel="ussd",
                language=farmer.language_preference,
                farmer_context={
                    "location": farmer.location,
                    "crop": farmer.primary_crop,
                }
            )
            
            # USSD format: CON for continue, END for end session
            response = f"CON {response_text}\n\nReply 0 for menu."
            
            # Log interaction
            interaction = Interaction(
                farmer_id=farmer.id,
                channel="ussd",
                user_message=user_input,
                bot_response=response_text,
                response_tokens=tokens,
                interaction_type="crop_advice"
            )
            db.add(interaction)
            db.commit()
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing USSD: {str(e)}")
        return f"END Error: {str(e)}\n"


def _build_main_menu() -> str:
    """Build main USSD menu"""
    return (
        "Agriculture Extension Bot\n"
        "1. Crop Advice\n"
        "2. Weather Alerts\n"
        "3. Market Prices\n"
        "4. Pest Info\n"
    )


def _build_crop_menu() -> str:
    """Build crop selection menu"""
    return (
        "Choose crop:\n"
        "1. Maize\n"
        "2. Beans\n"
        "3. Potatoes\n"
        "4. Wheat\n"
        "0. Main menu\n"
    )
