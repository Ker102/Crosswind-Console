"""
Trip Planner API Router - Endpoints for multi-step travel planning.
"""
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..services.trip_planner import get_trip_planner, TripPlannerResult


router = APIRouter(prefix="/trip-planner", tags=["trip-planner"])


# =============================================================================
# Request/Response Models
# =============================================================================

class TripPlanRequest(BaseModel):
    """Request model for trip planning."""
    origin: str = Field(..., description="Origin IATA code (e.g., LHR)")
    destination: str = Field(..., description="Destination IATA code (e.g., CDG)")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    travelers: int = Field(default=1, description="Number of travelers")
    budget: Optional[float] = Field(default=None, description="Budget constraint")
    preferences: Optional[List[str]] = Field(default=None, description="User preferences")


class TripPlanResponse(BaseModel):
    """Response model for trip planning."""
    success: bool
    itinerary: Optional[str]
    flights_count: int
    hotels_count: int
    messages: List[str]
    errors: List[str]


# =============================================================================
# Endpoints
# =============================================================================

@router.post("/start", response_model=TripPlanResponse)
async def start_trip_planning(request: TripPlanRequest) -> TripPlanResponse:
    """
    Start a new trip planning session.
    
    This executes the LangGraph workflow:
    1. Parse intent
    2. Search flights (Amadeus)
    3. Search hotels (Amadeus)
    4. Rank and recommend options
    
    Returns an itinerary with recommended flight + hotel.
    """
    planner = get_trip_planner()
    
    result: TripPlannerResult = await planner.plan_trip(
        origin=request.origin,
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        travelers=request.travelers,
        budget=request.budget,
        preferences=request.preferences
    )
    
    return TripPlanResponse(
        success=result.success,
        itinerary=result.itinerary,
        flights_count=len(result.flights),
        hotels_count=len(result.hotels),
        messages=result.messages,
        errors=result.errors
    )


@router.get("/health")
async def trip_planner_health():
    """Health check for trip planner service."""
    return {"status": "ok", "service": "trip-planner", "version": "1.0.0"}
