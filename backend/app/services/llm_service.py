"""
LLM Service - Handles OpenAI API calls and response generation
"""
import logging
import re
from typing import Optional, Dict, Any
from openai import OpenAI, APIError, RateLimitError
from app.core.config import settings
from app.core.prompts import get_system_prompt, build_context

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM interactions"""
    
    def __init__(self):
        """Initialize LLM client"""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
    
    def generate_response(
        self,
        user_message: str,
        channel: str = "web",
        language: str = "english",
        farmer_context: Optional[Dict[str, Any]] = None,
        weather_data: Optional[Dict[str, Any]] = None,
        market_data: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, int]:
        """
        Generate response using LLM
        
        Args:
            user_message: User's query
            channel: Communication channel (sms, ussd, voice, web)
            language: Language preference (english, sesotho)
            farmer_context: Farmer profile info
            weather_data: Current weather data
            market_data: Market price data
            
        Returns:
            Tuple of (response_text, token_count)
        """
        if not self.client:
            logger.error("LLM client not initialized")
            return self._get_fallback_response(user_message, channel), 0
        
        try:
            # Build contextual information
            context = build_context(farmer_context, weather_data, market_data)
            
            # Format message based on channel constraints
            formatted_message = self._format_for_channel(user_message, channel)
            
            # Build messages for API
            messages = [
                {
                    "role": "system",
                    "content": get_system_prompt() + context
                },
                {
                    "role": "user",
                    "content": f"[{channel.upper()}] [{language.upper()}] {formatted_message}"
                }
            ]
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                max_tokens=self._get_max_tokens(channel),
                temperature=0.7,
            )
            
            # Extract response
            bot_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Format response for channel
            bot_response = self._format_response_for_channel(bot_response, channel)
            
            logger.info(f"Generated response for {channel} channel, tokens: {tokens_used}")
            return bot_response, tokens_used
            
        except RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            return self._get_fallback_response(user_message, channel, "rate_limit"), 0
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._get_fallback_response(user_message, channel, "api_error"), 0
        except Exception as e:
            logger.error(f"Unexpected error in LLM: {str(e)}")
            return self._get_fallback_response(user_message, channel, "unknown"), 0
    
    def _format_for_channel(self, message: str, channel: str) -> str:
        """Format message based on channel type"""
        if channel == "sms":
            # Remove special characters for SMS
            message = re.sub(r'[^a-zA-Z0-9\s\.\,\?\!]', '', message)
        elif channel == "ussd":
            # USSD has very limited character support
            message = message[:160]
        elif channel == "voice":
            # Voice can handle natural language
            pass
        return message
    
    def _get_max_tokens(self, channel: str) -> int:
        """Get max tokens based on channel constraints"""
        return {
            "sms": 160,     # SMS limit
            "ussd": 182,    # USSD limit
            "voice": 500,   # Voice can be longer
            "web": 2000,    # Web has no hard limit
        }.get(channel, 500)
    
    def _format_response_for_channel(self, response: str, channel: str) -> str:
        """Format response for channel constraints"""
        if channel == "sms":
            # Truncate to SMS limit
            if len(response) > 160:
                response = response[:157] + "..."
        elif channel == "ussd":
            # USSD menu format
            if len(response) > 182:
                response = response[:179] + "..."
        elif channel == "voice":
            # Keep as is, TTS will handle
            pass
        
        return response
    
    def _get_fallback_response(self, user_message: str, channel: str, error_type: str = None) -> str:
        """Get fallback response when LLM is unavailable"""
        fallback_responses = {
            "rate_limit": "Our service is currently busy. Please try again in a few minutes.",
            "api_error": "Sorry, I'm having trouble connecting to my knowledge base. Please try again later.",
            "unknown": "I apologize, but I couldn't process your request. Please try rephrasing.",
            None: self._generate_rule_based_response(user_message)
        }
        return fallback_responses.get(error_type, fallback_responses[None])
    
    def _generate_rule_based_response(self, message: str) -> str:
        """Generate rule-based response when LLM unavailable"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["pest", "armyworm", "grasshopper"]):
            return "For pest issues, spray with approved organic pesticide. Remove affected plants. Contact local extension office for support."
        elif any(word in message_lower for word in ["drought", "water", "rain"]):
            return "During drought: water early morning/evening, mulch crops, use drought-resistant varieties. Check weather forecast regularly."
        elif any(word in message_lower for word in ["price", "market", "sell"]):
            return "Market prices vary by location and season. Contact your local market or cooperative for current prices."
        elif any(word in message_lower for word in ["plant", "seed", "crop"]):
            return "For crop advice, tell me: what crop, growth stage, and any problems you see. I'll provide specific guidance."
        else:
            return "I'm here to help with farming advice. Ask about crops, pests, weather, or market prices."
