"""
Test script to verify Amadeus Flight API integration in travel_server.py
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

async def test_amadeus():
    print("=" * 60)
    print("Testing Amadeus Flight Search Integration")
    print("=" * 60)
    
    # Check credentials are loaded
    client_id = os.getenv("AMADEUS_CLIENT_ID", "")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "")
    
    print(f"\n1. Checking credentials...")
    print(f"   Client ID: {client_id[:10]}..." if client_id else "   ❌ Client ID not set!")
    print(f"   Client Secret: {client_secret[:5]}..." if client_secret else "   ❌ Client Secret not set!")
    
    if not client_id or not client_secret:
        print("\n❌ Credentials not found. Please check .env file.")
        return
    
    # Import and test
    print(f"\n2. Testing OAuth2 token retrieval...")
    try:
        from travel_server import _get_amadeus_token
        token = await _get_amadeus_token()
        print(f"   ✅ Token received: {token[:20]}...")
    except Exception as e:
        print(f"   ❌ Token error: {e}")
        return
    
    print(f"\n3. Testing flight search (LHR → JFK, 2026-04-20)...")
    try:
        from travel_server import search_amadeus_flights
        result = await search_amadeus_flights(
            from_location="LHR",
            to_location="JFK",
            date="2026-04-20",
            adults=1
        )
        print(result)
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return
    
    print("\n✅ Amadeus integration verified successfully!")

if __name__ == "__main__":
    asyncio.run(test_amadeus())
