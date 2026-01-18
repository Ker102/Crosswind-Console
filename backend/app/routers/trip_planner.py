"""
Trip Planner API Router - Endpoints for multi-step travel planning.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.trip_planner import get_trip_planner, TripPlannerResult
from ..services.session_storage import get_session_storage, TripSession


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
    user_id: Optional[str] = Field(default=None, description="User ID for session persistence")
    save_session: bool = Field(default=True, description="Whether to save session to database")


class TripPlanResponse(BaseModel):
    """Response model for trip planning."""
    success: bool
    session_id: Optional[str] = None
    itinerary: Optional[str]
    flights_count: int
    hotels_count: int
    messages: List[str]
    errors: List[str]


class SessionResponse(BaseModel):
    """Response model for session operations."""
    session_id: str
    user_id: Optional[str]
    phase: str
    is_complete: bool
    state: dict


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    sessions: List[SessionResponse]
    count: int


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
    If save_session=True, the session is persisted to Supabase.
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
    
    session_id = None
    
    # Save session if requested
    if request.save_session:
        try:
            storage = get_session_storage()
            state = {
                "origin": request.origin,
                "destination": request.destination,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "travelers": request.travelers,
                "budget": request.budget,
                "preferences": request.preferences or [],
                "flights": result.flights,
                "hotels": result.hotels,
                "itinerary": result.itinerary,
                "phase": "complete" if result.success else "error",
                "messages": result.messages,
                "errors": result.errors
            }
            session_id = await storage.create_session(state, request.user_id)
        except Exception as e:
            # Don't fail the request if session save fails
            result.errors.append(f"Session save failed: {str(e)}")
    
    return TripPlanResponse(
        success=result.success,
        session_id=session_id,
        itinerary=result.itinerary,
        flights_count=len(result.flights),
        hotels_count=len(result.hotels),
        messages=result.messages,
        errors=result.errors
    )


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str) -> SessionResponse:
    """
    Retrieve a trip planning session by ID.
    """
    storage = get_session_storage()
    session = await storage.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        session_id=session.session_id,
        user_id=session.user_id,
        phase=session.phase,
        is_complete=session.is_complete,
        state=session.state
    )


@router.get("/sessions/{user_id}", response_model=SessionListResponse)
async def list_user_sessions(
    user_id: str,
    limit: int = 10,
    include_complete: bool = False
) -> SessionListResponse:
    """
    List all trip planning sessions for a user.
    """
    storage = get_session_storage()
    sessions = await storage.list_user_sessions(user_id, limit, include_complete)
    
    return SessionListResponse(
        sessions=[
            SessionResponse(
                session_id=s.session_id,
                user_id=s.user_id,
                phase=s.phase,
                is_complete=s.is_complete,
                state=s.state
            )
            for s in sessions
        ],
        count=len(sessions)
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str) -> dict:
    """
    Delete a trip planning session.
    """
    storage = get_session_storage()
    success = await storage.delete_session(session_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"success": True, "message": "Session deleted"}


@router.get("/health")
async def trip_planner_health():
    """Health check for trip planner service."""
    return {"status": "ok", "service": "trip-planner", "version": "1.1.0"}

