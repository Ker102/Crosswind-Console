import asyncio
from dotenv import load_dotenv
load_dotenv('../.env')
import os
import sys
sys.path.insert(0, '../mcp_servers')
from travel_server import search_flights_sky

async def main():
    print("Testing search_flights_sky with Google Flights2 API...")
    # Use a date in 2026
    result = await search_flights_sky(
        from_location="LHR", 
        to_location="JFK", 
        date="2026-04-20",
        adults=1
    )
    print("\nResult:")
    print(f"Type: {type(result)}")
    print(f"Content: {repr(result)}")

if __name__ == "__main__":
    asyncio.run(main())
