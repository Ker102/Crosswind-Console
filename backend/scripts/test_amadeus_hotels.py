"""
Test script to verify Amadeus Hotel API integration in travel_server.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for mcp_servers import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp_servers"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

async def test_amadeus_hotels():
    print("=" * 60)
    print("Testing Amadeus Hotel Search Integration")
    print("=" * 60)
    
    print(f"\n1. Testing hotel search in Paris (PAR)...")
    try:
        from travel_server import search_amadeus_hotels
        result = await search_amadeus_hotels(
            city_code="PAR",
            check_in_date="2026-04-20",
            check_out_date="2026-04-25",
            adults=2,
            rooms=1
        )
        print(result)
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n✅ Amadeus Hotels integration test complete!")

if __name__ == "__main__":
    asyncio.run(test_amadeus_hotels())
