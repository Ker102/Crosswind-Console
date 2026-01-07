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
        'x-rapidapi-host': 'sky-scrapper.p.rapidapi.com'
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get airport IDs - use major route for testing
        r1 = await client.get('https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport', headers=headers, params={'query': 'London'})
        origin = r1.json()['data'][0]
        print(f"Origin: skyId={origin.get('skyId')}, entityId={origin.get('entityId')}")
        
        r2 = await client.get('https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport', headers=headers, params={'query': 'New York'})
        dest = r2.json()['data'][0]
        print(f"Dest: skyId={dest.get('skyId')}, entityId={dest.get('entityId')}")
        
        # Search flights
        params = {
            'originSkyId': origin.get('skyId'),
            'destinationSkyId': dest.get('skyId'),
            'originEntityId': origin.get('entityId'),
            'destinationEntityId': dest.get('entityId'),
            'date': '2025-04-20',
            'adults': '1',
            'currency': 'USD',
            'market': 'US',
            'locale': 'en-US'
        }
        print(f"Search params: {params}")
        r3 = await client.get('https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights', headers=headers, params=params)
        data = r3.json()
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        if isinstance(data.get('data'), dict):
            print(f"Data keys: {list(data.get('data', {}).keys())}")
            itins = data.get('data', {}).get('itineraries', [])
            print(f"Found {len(itins)} itineraries")
            
            # Check context for session/status
            context = data.get('data', {}).get('context', {})
            print(f"Context: {context}")
            
            # Check for filterStats which sometimes contains flight info
            filter_stats = data.get('data', {}).get('filterStats', {})
            print(f"Filter stats duration: {filter_stats.get('duration')}")
            
            # Check session ID for polling
            session_id = data.get('data', {}).get('flightsSessionId')
            print(f"Session ID: {session_id}")
            
            # If incomplete, try polling
            if session_id:
                print("\\n--- Trying to poll for complete results ---")
                import asyncio
                await asyncio.sleep(2)
                poll_r = await client.get(
                    'https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlightsComplete',
                    headers=headers,
                    params={'sessionId': session_id}
                )
                poll_data = poll_r.json()
                poll_itins = poll_data.get('data', {}).get('itineraries', [])
                print(f"Poll results: {len(poll_itins)} itineraries")
                if poll_itins:
                    print(f"First itinerary: {json.dumps(poll_itins[0], indent=2)[:1000]}")
            
            if itins:
                print(f"First itin: {json.dumps(itins[0], indent=2)[:500]}")
        else:
            print(f"Data type: {type(data.get('data'))}")
            print(f"Raw response: {json.dumps(data, indent=2)}")

asyncio.run(test())
