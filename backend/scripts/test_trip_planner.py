"""
Test script for Trip Planner Agent.
"""
import asyncio
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")


async def test_trip_planner():
    print("=" * 60)
    print("Testing Trip Planner Agent (LangGraph)")
    print("=" * 60)
    
    from app.services.trip_planner import get_trip_planner
    
    planner = get_trip_planner()
    
    print("\n1. Planning trip: London → Paris")
    print("   Dates: 2026-04-20 to 2026-04-25")
    print("   Travelers: 2")
    
    result = await planner.plan_trip(
        origin="LHR",
        destination="CDG",
        start_date="2026-04-20",
        end_date="2026-04-25",
        travelers=2
    )
    
    print("\n--- Results ---")
    print(f"Success: {result.success}")
    print(f"Flights found: {len(result.flights)}")
    print(f"Hotels found: {len(result.hotels)}")
    print(f"\nMessages:")
    for msg in result.messages:
        print(f"  {msg}")
    
    if result.errors:
        print(f"\nErrors:")
        for err in result.errors:
            print(f"  ⚠️ {err}")
    
    print(f"\n--- Itinerary ---")
    print(result.itinerary or "No itinerary generated")
    
    print("\n✅ Trip Planner test complete!")


if __name__ == "__main__":
    asyncio.run(test_trip_planner())
