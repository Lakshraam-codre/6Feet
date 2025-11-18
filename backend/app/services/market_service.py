"""
Market Service - Handles market price data management
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import MarketPrice
from app.schemas.schemas import MarketPriceCreate, MarketPriceResponse

logger = logging.getLogger(__name__)


class MarketService:
    """Service for market data operations"""
    
    # Common Lesotho crops with typical price ranges
    LESOTHO_CROPS = {
        "maize": {"currency": "LSL", "unit": "kg"},
        "wheat": {"currency": "LSL", "unit": "kg"},
        "sorghum": {"currency": "LSL", "unit": "kg"},
        "beans": {"currency": "LSL", "unit": "kg"},
        "potatoes": {"currency": "LSL", "unit": "kg"},
        "cabbage": {"currency": "LSL", "unit": "kg"},
    }
    
    @staticmethod
    def get_market_price(db: Session, crop_name: str, location: Optional[str] = None) -> Optional[MarketPriceResponse]:
        """
        Get latest market price for a crop
        
        Args:
            db: Database session
            crop_name: Name of crop
            location: Optional location filter
            
        Returns:
            MarketPriceResponse or None
        """
        try:
            query = db.query(MarketPrice).filter(
                MarketPrice.crop_name.ilike(crop_name)
            )
            
            if location:
                query = query.filter(MarketPrice.location.ilike(location))
            
            # Get most recent price
            price = query.order_by(MarketPrice.last_updated.desc()).first()
            
            if price:
                logger.info(f"Found market price for {crop_name} in {location or 'any location'}")
                return MarketPriceResponse.from_orm(price)
            
            logger.warning(f"No market price found for {crop_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching market price: {str(e)}")
            return None
    
    @staticmethod
    def get_prices_by_location(db: Session, location: str) -> List[MarketPriceResponse]:
        """
        Get all market prices for a location
        
        Args:
            db: Database session
            location: Location name
            
        Returns:
            List of MarketPriceResponse
        """
        try:
            prices = db.query(MarketPrice).filter(
                MarketPrice.location.ilike(location)
            ).order_by(MarketPrice.last_updated.desc()).all()
            
            return [MarketPriceResponse.from_orm(p) for p in prices]
        except Exception as e:
            logger.error(f"Error fetching prices for location: {str(e)}")
            return []
    
    @staticmethod
    def create_market_price(db: Session, price_data: MarketPriceCreate) -> Optional[MarketPriceResponse]:
        """
        Create or update market price
        
        Args:
            db: Database session
            price_data: Price data to create
            
        Returns:
            Created MarketPriceResponse or None
        """
        try:
            # Check if price exists
            existing = db.query(MarketPrice).filter(
                MarketPrice.crop_name.ilike(price_data.crop_name),
                MarketPrice.location.ilike(price_data.location)
            ).first()
            
            if existing:
                # Update existing
                existing.price_per_kg = price_data.price_per_kg
                existing.demand_level = price_data.demand_level
                existing.best_selling_period = price_data.best_selling_period
                existing.last_updated = datetime.utcnow()
                db.commit()
                logger.info(f"Updated market price for {price_data.crop_name} in {price_data.location}")
                return MarketPriceResponse.from_orm(existing)
            else:
                # Create new
                new_price = MarketPrice(**price_data.dict())
                db.add(new_price)
                db.commit()
                logger.info(f"Created market price for {price_data.crop_name}")
                return MarketPriceResponse.from_orm(new_price)
                
        except Exception as e:
            logger.error(f"Error creating market price: {str(e)}")
            db.rollback()
            return None
    
    @staticmethod
    def get_best_selling_time(crop_name: str) -> str:
        """
        Get best selling season for a crop (Lesotho-specific)
        
        Args:
            crop_name: Crop name
            
        Returns:
            String describing best selling time
        """
        selling_seasons = {
            "maize": "May-July (after harvest)",
            "wheat": "August-October (after harvest)",
            "potatoes": "March-May",
            "cabbage": "April-August",
            "beans": "July-September",
            "sorghum": "June-August",
        }
        return selling_seasons.get(crop_name.lower(), "After harvest season")
    
    @staticmethod
    def get_market_summary(db: Session) -> Dict[str, Any]:
        """
        Get summary of all market prices
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with market summary
        """
        try:
            prices = db.query(MarketPrice).filter(
                MarketPrice.last_updated > datetime.utcnow() - timedelta(days=7)
            ).all()
            
            summary = {}
            for price in prices:
                if price.crop_name not in summary:
                    summary[price.crop_name] = []
                summary[price.crop_name].append({
                    "location": price.location,
                    "price_per_kg": price.price_per_kg,
                    "demand": price.demand_level,
                })
            
            return summary
        except Exception as e:
            logger.error(f"Error generating market summary: {str(e)}")
            return {}
