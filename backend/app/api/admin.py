"""
Admin API routes for managing farmers, market prices, and alerts
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Farmer, MarketPrice, Alert, CropSession
from app.schemas.schemas import (
    FarmerCreate, FarmerUpdate, FarmerResponse,
    MarketPriceCreate, MarketPriceResponse,
    AlertCreate, AlertResponse,
    CropSessionCreate, CropSessionResponse
)
from app.services.market_service import MarketService
from app.services.africas_talking_service import AfricasTalkingService
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["Admin"])
at_service = AfricasTalkingService()
logger = logging.getLogger(__name__)


# Farmer management
@router.get("/farmers", response_model=List[FarmerResponse])
async def list_farmers(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get list of farmers"""
    try:
        farmers = db.query(Farmer).offset(skip).limit(limit).all()
        return farmers
    except Exception as e:
        logger.error(f"Error listing farmers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/farmers/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Get specific farmer"""
    try:
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise HTTPException(status_code=404, detail="Farmer not found")
        return farmer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting farmer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/farmers", response_model=FarmerResponse)
async def create_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    """Create new farmer"""
    try:
        # Check if farmer already exists
        existing = db.query(Farmer).filter(Farmer.phone_number == farmer.phone_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Farmer already exists")
        
        new_farmer = Farmer(**farmer.dict())
        db.add(new_farmer)
        db.commit()
        db.refresh(new_farmer)
        
        logger.info(f"New farmer created: {new_farmer.id}")
        return new_farmer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating farmer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/farmers/{farmer_id}", response_model=FarmerResponse)
async def update_farmer(farmer_id: int, farmer: FarmerUpdate, db: Session = Depends(get_db)):
    """Update farmer profile"""
    try:
        db_farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not db_farmer:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        farmer_data = farmer.dict(exclude_unset=True)
        for key, value in farmer_data.items():
            setattr(db_farmer, key, value)
        
        db.commit()
        db.refresh(db_farmer)
        
        logger.info(f"Farmer {farmer_id} updated")
        return db_farmer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating farmer: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Market price management
@router.get("/market-prices", response_model=List[MarketPriceResponse])
async def list_market_prices(db: Session = Depends(get_db), crop: str = None, location: str = None):
    """List market prices with optional filters"""
    try:
        query = db.query(MarketPrice)
        if crop:
            query = query.filter(MarketPrice.crop_name.ilike(f"%{crop}%"))
        if location:
            query = query.filter(MarketPrice.location.ilike(f"%{location}%"))
        
        prices = query.order_by(MarketPrice.last_updated.desc()).all()
        return prices
    except Exception as e:
        logger.error(f"Error listing market prices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/market-prices", response_model=MarketPriceResponse)
async def create_market_price(price: MarketPriceCreate, db: Session = Depends(get_db)):
    """Create or update market price"""
    try:
        result = MarketService.create_market_price(db, price)
        if result:
            logger.info(f"Market price created/updated for {price.crop_name}")
            return result
        raise HTTPException(status_code=400, detail="Failed to create market price")
    except Exception as e:
        logger.error(f"Error creating market price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/market-prices/{price_id}")
async def delete_market_price(price_id: int, db: Session = Depends(get_db)):
    """Delete market price"""
    try:
        price = db.query(MarketPrice).filter(MarketPrice.id == price_id).first()
        if not price:
            raise HTTPException(status_code=404, detail="Price not found")
        
        db.delete(price)
        db.commit()
        
        logger.info(f"Market price {price_id} deleted")
        return {"status": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting market price: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Alert management
@router.post("/alerts", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create new alert"""
    try:
        new_alert = Alert(**alert.dict())
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        logger.info(f"Alert created: {new_alert.id}")
        return new_alert
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/send-bulk")
async def send_bulk_alerts(alert: AlertCreate, location_filter: str = None, db: Session = Depends(get_db)):
    """Send alert to multiple farmers"""
    try:
        # Get farmers to alert
        query = db.query(Farmer)
        if location_filter:
            query = query.filter(Farmer.location.ilike(f"%{location_filter}%"))
        
        farmers = query.all()
        
        # Send to each farmer
        success_count = 0
        for farmer in farmers:
            # Create alert record
            farmer_alert = Alert(
                farmer_id=farmer.id,
                alert_type=alert.alert_type,
                title=alert.title,
                message=alert.message,
                severity=alert.severity,
                action_recommended=alert.action_recommended,
                location=location_filter
            )
            db.add(farmer_alert)
            
            # Send SMS if phone available
            if farmer.phone_number:
                message = f"{alert.title}: {alert.message}"
                success = await at_service.send_sms(farmer.phone_number, message)
                if success:
                    success_count += 1
                    farmer_alert.is_sent = True
                    farmer_alert.sent_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Bulk alert sent to {success_count}/{len(farmers)} farmers")
        return {
            "total_farmers": len(farmers),
            "successfully_sent": success_count,
            "failed": len(farmers) - success_count
        }
    except Exception as e:
        logger.error(f"Error sending bulk alerts: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Crop session management
@router.post("/crop-sessions", response_model=CropSessionResponse)
async def create_crop_session(session: CropSessionCreate, db: Session = Depends(get_db)):
    """Create new crop session for farmer"""
    try:
        from app.models.models import CropSession
        new_session = CropSession(**session.dict())
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        logger.info(f"Crop session created: {new_session.id}")
        return new_session
    except Exception as e:
        logger.error(f"Error creating crop session: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Analytics endpoints
@router.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        from app.models.models import Interaction, Farmer, MarketPrice, Alert
        
        total_farmers = db.query(Farmer).count()
        total_interactions = db.query(Interaction).count()
        total_alerts = db.query(Alert).filter(Alert.is_sent == True).count()
        total_prices = db.query(MarketPrice).count()
        
        return {
            "total_farmers": total_farmers,
            "total_interactions": total_interactions,
            "total_alerts_sent": total_alerts,
            "market_prices": total_prices,
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
