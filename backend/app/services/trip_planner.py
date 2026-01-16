"""
Trip Planner Agent - LangGraph-based multi-step travel planning.
Phase 1: Basic graph with flight + hotel search pipeline.
"""
import os
import re
from typing import TypedDict, List, Optional, Annotated
from operator import add
from dataclasses import dataclass
from datetime import datetime

from langgraph.graph import StateGraph, END

# Import existing tools (same pattern as llm.py)
try:
    from mcp_servers.travel_server import search_amadeus_flights, search_amadeus_hotels
except ImportError:
    # Fallback - tools will return errors
    async def search_amadeus_flights(*args, **kwargs):
        return "Error: Amadeus tools not available"
    async def search_amadeus_hotels(*args, **kwargs):
        return "Error: Amadeus tools not available"


# =============================================================================
# State Schema
# =============================================================================

class TripState(TypedDict):
    """State that flows through the trip planning graph."""
    
    # User inputs (parsed from natural language)
    destination: str
    origin: str
    start_date: str
    end_date: str
    travelers: int
    budget: Optional[float]
    preferences: List[str]
    
    # Search results (accumulated via Annotated[..., add])
    flights: Annotated[List[dict], add]
    hotels: Annotated[List[dict], add]
    
    # Ranked/selected options
    recommended_flight: Optional[dict]
    recommended_hotel: Optional[dict]
    
    # Workflow state
    phase: str  # "parsing", "searching", "ranking", "complete"
    messages: Annotated[List[str], add]
    errors: Annotated[List[str], add]
    
    # Final output
    itinerary: Optional[str]


# =============================================================================
# Graph Nodes
# =============================================================================

async def parse_intent(state: TripState) -> dict:
    """
    Extract trip parameters from natural language input.
    For Phase 1, we expect structured input; this is a placeholder for LLM parsing.
    """
    # In Phase 1, we assume the state is already populated with structured data
    # In Phase 2, we'll use Gemini to parse natural language
    
    messages = [f"✅ Intent parsed: {state.get('origin', '?')} → {state.get('destination', '?')}"]
    
    return {
        "phase": "searching",
        "messages": messages
    }


async def search_flights_node(state: TripState) -> dict:
    """Search for flights using Amadeus API."""
    
    origin = state.get("origin", "")
    destination = state.get("destination", "")
    start_date = state.get("start_date", "")
    travelers = state.get("travelers", 1)
    
    if not all([origin, destination, start_date]):
        return {
            "errors": ["Missing required flight search parameters"],
            "flights": []
        }
    
    try:
        # Call Amadeus flight search with correct parameter names
        result = await search_amadeus_flights(
            from_location=origin,
            to_location=destination,
            date=start_date,
            adults=travelers,
            max_results=5
        )
        
        # Parse the result (it's a string from the MCP tool)
        flights = []
        if "Error" not in result:
            # Parse the formatted output
            for line in result.split("\n"):
                if line.strip() and not line.startswith("Found"):
                    flights.append({"raw": line.strip()})
        
        return {
            "flights": flights,
            "messages": [f"✈️ Found {len(flights)} flight options"]
        }
        
    except Exception as e:
        return {
            "errors": [f"Flight search failed: {str(e)}"],
            "flights": []
        }


async def search_hotels_node(state: TripState) -> dict:
    """Search for hotels using Amadeus API."""
    
    destination = state.get("destination", "")
    start_date = state.get("start_date", "")
    end_date = state.get("end_date", "")
    travelers = state.get("travelers", 1)
    
    if not all([destination, start_date, end_date]):
        return {
            "errors": ["Missing required hotel search parameters"],
            "hotels": []
        }
    
    try:
        # Call Amadeus hotel search with correct parameter names
        result = await search_amadeus_hotels(
            city_code=destination,
            check_in_date=start_date,
            check_out_date=end_date,
            adults=travelers,
            rooms=1,
            max_results=5
        )
        
        # Parse the result
        hotels = []
        if "Error" not in result:
            for line in result.split("\n"):
                if line.strip() and not line.startswith("Found"):
                    hotels.append({"raw": line.strip()})
        
        return {
            "hotels": hotels,
            "messages": [f"🏨 Found {len(hotels)} hotel options"]
        }
        
    except Exception as e:
        return {
            "errors": [f"Hotel search failed: {str(e)}"],
            "hotels": []
        }


async def rank_options(state: TripState) -> dict:
    """
    Rank and recommend the best flight + hotel combination.
    Phase 1: Simple selection (first available).
    Phase 2: LLM-based ranking with user preferences.
    """
    
    flights = state.get("flights", [])
    hotels = state.get("hotels", [])
    
    recommended_flight = flights[0] if flights else None
    recommended_hotel = hotels[0] if hotels else None
    
    # Generate simple itinerary
    itinerary_parts = []
    itinerary_parts.append(f"📍 Trip: {state.get('origin', '?')} → {state.get('destination', '?')}")
    itinerary_parts.append(f"📅 Dates: {state.get('start_date', '?')} to {state.get('end_date', '?')}")
    itinerary_parts.append(f"👥 Travelers: {state.get('travelers', 1)}")
    itinerary_parts.append("")
    
    if recommended_flight:
        itinerary_parts.append(f"✈️ Recommended Flight:")
        itinerary_parts.append(f"   {recommended_flight.get('raw', 'N/A')}")
    else:
        itinerary_parts.append("✈️ No flights found")
    
    itinerary_parts.append("")
    
    if recommended_hotel:
        itinerary_parts.append(f"🏨 Recommended Hotel:")
        itinerary_parts.append(f"   {recommended_hotel.get('raw', 'N/A')}")
    else:
        itinerary_parts.append("🏨 No hotels found")
    
    return {
        "phase": "complete",
        "recommended_flight": recommended_flight,
        "recommended_hotel": recommended_hotel,
        "itinerary": "\n".join(itinerary_parts),
        "messages": ["🎯 Recommendations generated"]
    }


# =============================================================================
# Graph Definition
# =============================================================================

def create_trip_planner_graph():
    """Create and compile the trip planner workflow graph."""
    
    workflow = StateGraph(TripState)
    
    # Add nodes
    workflow.add_node("parse_intent", parse_intent)
    workflow.add_node("search_flights", search_flights_node)
    workflow.add_node("search_hotels", search_hotels_node)
    workflow.add_node("rank_options", rank_options)
    
    # Define edges (linear pipeline for Phase 1)
    workflow.set_entry_point("parse_intent")
    workflow.add_edge("parse_intent", "search_flights")
    workflow.add_edge("search_flights", "search_hotels")
    workflow.add_edge("search_hotels", "rank_options")
    workflow.add_edge("rank_options", END)
    
    # Phase 1: Compile without checkpointing (simpler, no persistence)
    # Phase 2 will add SqliteSaver for session persistence
    app = workflow.compile()
    
    return app


# =============================================================================
# Service Interface
# =============================================================================

@dataclass
class TripPlannerResult:
    """Result from trip planning execution."""
    success: bool
    itinerary: Optional[str]
    flights: List[dict]
    hotels: List[dict]
    messages: List[str]
    errors: List[str]


class TripPlannerService:
    """Service class for trip planning operations."""
    
    def __init__(self):
        self._graph = create_trip_planner_graph()
    
    async def plan_trip(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str,
        travelers: int = 1,
        budget: Optional[float] = None,
        preferences: Optional[List[str]] = None
    ) -> TripPlannerResult:
        """
        Execute the trip planning workflow.
        
        Args:
            origin: Origin IATA code (e.g., "LHR")
            destination: Destination IATA code (e.g., "CDG")
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            travelers: Number of travelers
            budget: Optional budget constraint
            preferences: Optional list of preferences
        
        Returns:
            TripPlannerResult with itinerary and search results
        """
        
        # Initialize state
        initial_state: TripState = {
            "origin": origin.upper(),
            "destination": destination.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "travelers": travelers,
            "budget": budget,
            "preferences": preferences or [],
            "flights": [],
            "hotels": [],
            "recommended_flight": None,
            "recommended_hotel": None,
            "phase": "parsing",
            "messages": [],
            "errors": [],
            "itinerary": None
        }
        
        try:
            # Execute the graph (no config needed without checkpointer)
            final_state = await self._graph.ainvoke(initial_state)
            
            return TripPlannerResult(
                success=len(final_state.get("errors", [])) == 0,
                itinerary=final_state.get("itinerary"),
                flights=final_state.get("flights", []),
                hotels=final_state.get("hotels", []),
                messages=final_state.get("messages", []),
                errors=final_state.get("errors", [])
            )
            
        except Exception as e:
            return TripPlannerResult(
                success=False,
                itinerary=None,
                flights=[],
                hotels=[],
                messages=[],
                errors=[f"Trip planning failed: {str(e)}"]
            )


# Singleton instance
_trip_planner: Optional[TripPlannerService] = None

def get_trip_planner() -> TripPlannerService:
    """Get singleton trip planner instance."""
    global _trip_planner
    if _trip_planner is None:
        _trip_planner = TripPlannerService()
    return _trip_planner
