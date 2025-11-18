"""
SMS Channel - Africa's Talking SMS webhook endpoints
"""
import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Farmer, Interaction
from app.schemas.schemas import SMSRequest
from app.services.llm_service import LLMService
from app.services.africas_talking_service import AfricasTalkingService
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/channels/sms", tags=["SMS"])
llm_service = LLMService()
at_service = AfricasTalkingService()
logger = logging.getLogger(__name__)


@router.post("/webhook")
async def sms_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook to receive SMS from Africa's Talking
    
    Expects form data:
    - phoneNumber: Sender's phone number
    - text: Message text
    - linkId: Message ID
    - date: Timestamp
    - id: Africa's Talking ID
    """
    try:
        form_data = await request.form()
        
        phone_number = form_data.get("phoneNumber")
        user_message = form_data.get("text", "")
        link_id = form_data.get("linkId")
        
        if not phone_number or not user_message:
            return {"error": "Missing required fields"}
        
        logger.info(f"SMS received from {phone_number}: {user_message[:50]}")
        
        # Get or create farmer
        farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()
        if not farmer:
            farmer = Farmer(phone_number=phone_number, language_preference="english")
            db.add(farmer)
            db.commit()
            logger.info(f"New farmer registered: {phone_number}")
        
        # Update last interaction
        farmer.last_interaction = datetime.utcnow()
        db.commit()
        
        # Generate response using LLM
        response_text, tokens = llm_service.generate_response(
            user_message=user_message,
            channel="sms",
            language=farmer.language_preference,
            farmer_context={
                "location": farmer.location,
                "crop": farmer.primary_crop,
                "experience_level": farmer.farming_experience,
            }
        )
        
        # Ensure SMS length limit (160 chars per SMS, we'll keep it under 160)
        if len(response_text) > 160:
            response_text = response_text[:157] + "..."
        
        # Log interaction
        interaction = Interaction(
            farmer_id=farmer.id,
            channel="sms",
            user_message=user_message,
            bot_response=response_text,
            response_tokens=tokens,
            interaction_type="general"
        )
        db.add(interaction)
        db.commit()
        
        # Send response via Africa's Talking
        success = await at_service.send_sms(phone_number, response_text)
        
        if not success:
            logger.error(f"Failed to send SMS to {phone_number}")
        
        return {
            "status": "success",
            "message": response_text,
            "interaction_id": interaction.id
        }
        
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {str(e)}")
        return {"error": str(e), "status": "error"}


@router.post("/send")
async def send_sms(phone_number: str, message: str, db: Session = Depends(get_db)):
    """
    Send SMS to a farmer
    
    Args:
        phone_number: Recipient phone number
        message: Message to send
    """
    try:
        success = await at_service.send_sms(phone_number, message)
        
        if success:
            # Get farmer
            farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()
            if farmer:
                interaction = Interaction(
                    farmer_id=farmer.id,
                    channel="sms",
                    user_message="[SYSTEM]",
                    bot_response=message,
                    interaction_type="alert"
                )
                db.add(interaction)
                db.commit()
            
            return {"status": "success", "message": "SMS sent"}
        else:
            raise HTTPException(status_code=400, detail="Failed to send SMS")
            
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
