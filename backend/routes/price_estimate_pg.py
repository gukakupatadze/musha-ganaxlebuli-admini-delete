"""
Price Estimate API Routes - PostgreSQL Version
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime

from database import get_session

router = APIRouter()

# Price calculation constants (same as original)
BASE_PRICES = {
    'hdd': 100,
    'ssd': 150,
    'raid': 300,
    'usb': 50,
    'sd': 40,
    'other': 120
}

PROBLEM_MULTIPLIERS = {
    'logical': 1.0,
    'physical': 1.5,
    'water': 2.0,
    'fire': 2.5,
    'other': 1.2
}

URGENCY_MULTIPLIERS = {
    'standard': 1.0,
    'urgent': 1.5,
    'emergency': 2.0
}

TIMEFRAMES = {
    'standard': {'ka': 'სტანდარტული (5-7 დღე)', 'en': 'Standard (5-7 days)'},
    'urgent': {'ka': 'გადაუდებელი (2-3 დღე)', 'en': 'Urgent (2-3 days)'},
    'emergency': {'ka': 'საავარიო (24 საათი)', 'en': 'Emergency (24 hours)'}
}

# Pydantic models
class PriceEstimateRequest(BaseModel):
    device_type: str
    problem_type: str
    urgency: str

class PriceEstimateResponse(BaseModel):
    device_type: str
    problem_type: str
    urgency: str
    estimated_price: int
    timeframe_ka: str
    timeframe_en: str
    currency: str = "₾"

@router.post("/", response_model=PriceEstimateResponse)
async def calculate_price_estimate(
    request: PriceEstimateRequest,
    session: AsyncSession = Depends(get_session)
):
    """Calculate price estimate for data recovery service"""
    try:
        # Validate inputs
        if request.device_type not in BASE_PRICES:
            raise HTTPException(status_code=400, detail="Invalid device type")
        
        if request.problem_type not in PROBLEM_MULTIPLIERS:
            raise HTTPException(status_code=400, detail="Invalid problem type")
        
        if request.urgency not in URGENCY_MULTIPLIERS:
            raise HTTPException(status_code=400, detail="Invalid urgency level")
        
        # Calculate price
        base_price = BASE_PRICES[request.device_type]
        problem_multiplier = PROBLEM_MULTIPLIERS[request.problem_type]
        urgency_multiplier = URGENCY_MULTIPLIERS[request.urgency]
        
        estimated_price = int(base_price * problem_multiplier * urgency_multiplier)
        
        # Get timeframes
        timeframe = TIMEFRAMES[request.urgency]
        
        # Optionally store price estimate for analytics (future feature)
        # Could add a PriceEstimateSQL model and save the calculation
        
        return PriceEstimateResponse(
            device_type=request.device_type,
            problem_type=request.problem_type,
            urgency=request.urgency,
            estimated_price=estimated_price,
            timeframe_ka=timeframe['ka'],
            timeframe_en=timeframe['en'],
            currency="₾"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error calculating price estimate: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate price estimate")

@router.get("/configuration", response_model=dict)
async def get_price_configuration():
    """Get price calculation configuration for frontend"""
    return {
        "base_prices": BASE_PRICES,
        "problem_multipliers": PROBLEM_MULTIPLIERS,
        "urgency_multipliers": URGENCY_MULTIPLIERS,
        "timeframes": TIMEFRAMES
    }