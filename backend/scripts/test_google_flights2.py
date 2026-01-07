import asyncio
import httpx
import json
from dotenv import load_dotenv
load_dotenv('../.env')
import os

async def test():
    key = os.environ.get('RAPIDAPI_KEY')
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': 'google-flights2.p.rapidapi.com'
    }
    
    # Test 1: Simple One-Way Search
    print("Testing /search endpoint...")
    params = {
        'departure_id': 'LHR',
        'arrival_id': 'JFK',
        'outbound_date': '2026-04-20',
        'currency': 'USD',
        'hl': 'en',
        'type': '2' # Usually 2 is OneWay, 1 is RoundTrip in some Google APIs, or strings. Let's try strings first.
    }
    # Trying string type first which is more common in modern wrappers
    params['type'] = 'oneWay'
    
    endpoints = [
        '/api/v1/searchFlights', 
        '/api/v1/flights/search',
        '/api/v1/flight/search',
        '/flight/search', 
        '/flights/search',
        '/api/v1/search'
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for ep in endpoints:
            print(f"\nTesting {ep}...")
            url = f"https://google-flights2.p.rapidapi.com{ep}"
            try:
                r = await client.get(url, headers=headers, params=params)
                print(f"Status: {r.status_code}")
                if r.status_code != 404:
                    print(f"FOUND! Payload snippet: {r.text[:200]}")
                    try:
                        data = r.json()
                        # print("\nFull Response Structure:")
                        # print(json.dumps(data, indent=2)[:2000])
                        if isinstance(data.get("data"), list) and len(data["data"]) > 0:
                            first_item = data["data"][0]
                            print(f"\nFirst Flight Keys: {list(first_item.keys())}")
                            print(f"First Flight Sample: {json.dumps(first_item, indent=2)[:1000]}")
                    except:
                        pass
                    break
            except Exception as e:
                print(f"Error: {e}")

asyncio.run(test())
