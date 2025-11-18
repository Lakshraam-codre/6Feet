"""
Africa's Talking Integration Service
"""
import logging
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class AfricasTalkingService:
    """Service for Africa's Talking API interactions"""
    
    BASE_URL = "https://api.sandbox.africastalking.com"  # Use sandbox for testing
    
    def __init__(self):
        """Initialize Africa's Talking service"""
        self.api_key = settings.africas_talking_api_key
        self.username = settings.africas_talking_username
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "apiKey": self.api_key
        }
    
    async def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS via Africa's Talking
        
        Args:
            phone_number: Recipient phone number
            message: Message text
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api_key or not self.username:
            logger.warning("Africa's Talking credentials not configured")
            return False
        
        try:
            url = f"{self.BASE_URL}/version1/messaging"
            
            payload = {
                "username": self.username,
                "to": phone_number,
                "message": message,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=self.headers, timeout=10)
                
                if response.status_code == 201:
                    logger.info(f"SMS sent to {phone_number}")
                    return True
                else:
                    logger.error(f"SMS send failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False
    
    async def send_bulk_sms(self, recipients: list[str], message: str) -> int:
        """
        Send bulk SMS to multiple recipients
        
        Args:
            recipients: List of phone numbers
            message: Message text
            
        Returns:
            Number of successful sends
        """
        success_count = 0
        for phone in recipients:
            if await self.send_sms(phone, message):
                success_count += 1
        
        logger.info(f"Bulk SMS: {success_count}/{len(recipients)} sent successfully")
        return success_count
    
    async def initiate_ussd_session(self, phone_number: str, text: str = "") -> Optional[str]:
        """
        Initiate USSD session
        
        Args:
            phone_number: Phone number to send USSD to
            text: USSD text
            
        Returns:
            Session ID or None
        """
        if not self.api_key or not self.username:
            logger.warning("Africa's Talking credentials not configured")
            return None
        
        try:
            url = f"{self.BASE_URL}/version1/ussd/send"
            
            payload = {
                "username": self.username,
                "to": phone_number,
                "text": text,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=self.headers, timeout=10)
                
                if response.status_code == 201:
                    data = response.json()
                    session_id = data.get("sessionId")
                    logger.info(f"USSD session initiated: {session_id}")
                    return session_id
                else:
                    logger.error(f"USSD init failed: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error initiating USSD: {str(e)}")
            return None
    
    def build_ussd_menu(self, options: Dict[str, str], title: str = "Menu") -> str:
        """
        Build USSD menu response
        
        Args:
            options: Dictionary of option numbers to descriptions
            title: Menu title
            
        Returns:
            Formatted USSD menu
        """
        menu = f"{title}\n"
        for num, option in options.items():
            menu += f"{num}. {option}\n"
        menu += "Reply with option number"
        
        return menu
    
    def build_ussd_response(self, message: str, end_session: bool = False) -> str:
        """
        Build USSD response with proper formatting
        
        Args:
            message: Message to send
            end_session: Whether to end the session
            
        Returns:
            Formatted USSD response
        """
        # USSD responses have a 182 character limit
        if len(message) > 182:
            message = message[:179] + "..."
        
        return message
    
    async def initiate_call(self, phone_number: str) -> Optional[str]:
        """
        Initiate voice call
        
        Args:
            phone_number: Phone number to call
            
        Returns:
            Call SID or None
        """
        if not self.api_key or not self.username:
            logger.warning("Africa's Talking credentials not configured")
            return None
        
        try:
            url = f"{self.BASE_URL}/version1/voice/call"
            
            payload = {
                "username": self.username,
                "to": phone_number,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=self.headers, timeout=10)
                
                if response.status_code == 201:
                    data = response.json()
                    entries = data.get("entries", [])
                    if entries:
                        call_sid = entries[0].get("callSessionId")
                        logger.info(f"Call initiated: {call_sid}")
                        return call_sid
                else:
                    logger.error(f"Call initiation failed: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error initiating call: {str(e)}")
            return None
    
    def build_call_xml(self, message: str, hangup: bool = True) -> str:
        """
        Build XML for voice call response (Text-to-Speech and menu)
        
        Args:
            message: Message to speak
            hangup: Whether to hangup after message
            
        Returns:
            XML response
        """
        xml = f'<?xml version="1.0" encoding="UTF-8"?>'
        xml += f'<Response><Say>{message}</Say>'
        if hangup:
            xml += '<Hangup/>'
        xml += '</Response>'
        
        return xml
