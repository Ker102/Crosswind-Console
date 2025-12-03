import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("travel")

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
TRIPADVISOR_API_KEY = os.environ.get("TRIPADVISOR_API_KEY")
RAPIDAPI_HOST = "kiwi-com-cheap-flights.p.rapidapi.com"

@mcp.tool()
async def search_flights(from_location: str, to_location: str, date: str, return_date: str = None) -> str:
    """
    Search for flights using the Kiwi.com API via RapidAPI.
    
    Args:
        from_location: The IATA code or location ID for the departure airport (e.g., "LHR", "city:LON").
        to_location: The IATA code or location ID for the destination airport (e.g., "JFK", "city:NYC").
        date: The departure date in DD/MM/YYYY format.
        return_date: Optional return date in DD/MM/YYYY format.
    """
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY environment variable is not set."

    url = f"https://{RAPIDAPI_HOST}/search"
    
    querystring = {
        "fly_from": from_location,
        "fly_to": to_location,
        "date_from": date,
        "date_to": date,
        "curr": "USD",
        "sort": "price",
        "limit": "5"
    }

    if return_date:
        querystring["return_from"] = return_date
        querystring["return_to"] = return_date

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or not data["data"]:
                return "No flights found for the specified criteria."

            results = []
            for flight in data["data"]:
                price = flight.get("price", "N/A")
                currency = data.get("currency", "USD")
                deep_link = flight.get("deep_link", "")
                
                # Extract route details
                route_info = []
                for leg in flight.get("route", []):
                    airline = leg.get("airline", "Unknown")
                    flight_no = leg.get("flight_no", "")
                    dep_city = leg.get("cityFrom", "Unknown")
                    arr_city = leg.get("cityTo", "Unknown")
                    dep_time = leg.get("local_departure", "")
                    arr_time = leg.get("local_arrival", "")
                    route_info.append(f"{airline} {flight_no}: {dep_city} ({dep_time}) -> {arr_city} ({arr_time})")

                results.append(f"Price: {price} {currency}\nRoute: {' | '.join(route_info)}\nLink: {deep_link}\n---")

            return "\n".join(results)

        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

@mcp.tool()
async def search_places(query: str, category: str = "attractions", language: str = "en") -> str:
    """
    Search for places (hotels, restaurants, attractions) using TripAdvisor API.
    
    Args:
        query: Search query (e.g., "Eiffel Tower", "Sushi in Tokyo").
        category: Category filter ('hotels', 'attractions', 'restaurants', 'geos').
        language: Language code (default 'en').
    """
    if not TRIPADVISOR_API_KEY:
        return "Error: TRIPADVISOR_API_KEY is not set."

    url = "https://api.content.tripadvisor.com/api/v1/location/search"
    
    params = {
        "key": TRIPADVISOR_API_KEY,
        "searchQuery": query,
        "category": category,
        "language": language
    }

    headers = {"accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("data", [])[:5]: # Limit to 5
                name = item.get("name", "Unknown")
                address = item.get("address_obj", {}).get("address_string", "No address")
                location_id = item.get("location_id", "")
                # TripAdvisor content API often requires a second call for details/photos using location_id
                # For search, we just return the basic info found.
                results.append(f"Name: {name}\nAddress: {address}\nID: {location_id}\n---")
            
            if not results:
                return "No places found."
                
            return "\n".join(results)

        except Exception as e:
            return f"Error searching TripAdvisor: {str(e)}"

@mcp.tool()
async def search_hotels(latitude: float, longitude: float, checkin_date: str, checkout_date: str, adults: int = 1) -> str:
    """
    Search for hotels using Booking.com API (via RapidAPI).
    
    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        checkin_date: Check-in date (YYYY-MM-DD).
        checkout_date: Check-out date (YYYY-MM-DD).
        adults: Number of adults (default 1).
    """
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    # Booking.com API requires a location search first usually, but some endpoints accept lat/long.
    # The 'v1/hotels/search-by-coordinates' is a common pattern, but let's check if we can use the main search with lat/long.
    # Based on my verification, the main search takes dest_id. 
    # However, for efficiency, I will use the 'search-by-coordinates' if available, or I'll use a known pattern.
    # Actually, let's use the 'v1/hotels/search-by-coordinates' which is standard for this API family.
    # If that fails, I'll return a message.
    
    url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"
    
    querystring = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "adults_number": str(adults),
        "room_number": "1",
        "units": "metric",
        "order_by": "popularity"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "booking-com.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            results = []
            # Booking.com response structure usually has a 'result' key list
            hotels = data.get("result", [])
            for hotel in hotels[:5]:
                name = hotel.get("hotel_name", "Unknown")
                price = hotel.get("min_total_price", {}).get("value", "N/A")
                currency = hotel.get("currency_code", "USD")
                url_link = hotel.get("url", "")
                results.append(f"Hotel: {name}\nPrice: {price} {currency}\nLink: {url_link}\n---")
            
            if not results:
                return "No hotels found."
                
            return "\n".join(results)

        except Exception as e:
            return f"Error searching hotels: {str(e)}"

@mcp.tool()
async def search_flights_backup(from_entity: str, to_entity: str, date: str) -> str:
    """
    Backup flight search using Flights Sky (Skyscanner) API.
    
    Args:
        from_entity: Origin entity ID (e.g., "LOND-sky", "NYCA-sky").
        to_entity: Destination entity ID (e.g., "PARI-sky").
        date: Departure date (YYYY-MM-DD).
    """
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = "https://flights-sky.p.rapidapi.com/flights/search-one-way"
    
    # Note: This API requires specific Entity IDs. 
    # Ideally, we would have a helper tool to find these IDs first (e.g., /flights/auto-complete).
    # For this backup tool, we assume the LLM might try to guess or we provide common ones in prompt context.
    # Or better, we implement a quick lookup if needed, but for now keeping it simple as a backup.
    
    querystring = {
        "fromEntityId": from_entity,
        "toEntityId": to_entity,
        "departDate": date,
        "adults": "1",
        "currency": "USD",
        "market": "US",
        "locale": "en-US"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "flights-sky.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            # Parse response (structure varies, usually 'itineraries' or 'quotes')
            # Returning raw snippet for now as backup
            return str(data)[:2000]

        except Exception as e:
            return f"Error searching flights (backup): {str(e)}"

GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") # Using Maps key as it often covers Search too, or user should provide GOOGLE_API_KEY
GOOGLE_SEARCH_CX = os.environ.get("GOOGLE_SEARCH_CX")

@mcp.tool()
async def search_ground_transport(from_location: str, to_location: str, date: str) -> str:
    """
    Search for ground transport (bus, train) using Google Search restricted to aggregators.
    Returns deep links that can be scraped for details.
    
    Args:
        from_location: Departure city (e.g., "London").
        to_location: Destination city (e.g., "Paris").
        date: Travel date (e.g., "December 12, 2025").
    """
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_CX:
        return "Error: GOOGLE_MAPS_API_KEY or GOOGLE_SEARCH_CX is not set."

    query = f"bus or train from {from_location} to {to_location} on {date} site:rome2rio.com OR site:omio.com OR site:busbud.com"
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_CX,
        "q": query,
        "num": 5
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" not in data:
                return "No results found."

            results = []
            for item in data["items"]:
                title = item.get("title", "No title")
                link = item.get("link", "")
                snippet = item.get("snippet", "")
                results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n---")
            
            return "Found these routes. Use 'firecrawl' to scrape the links for details:\n\n" + "\n".join(results)

        except Exception as e:
            return f"Error searching ground transport: {str(e)}"

@mcp.tool()
async def search_ground_transport_backup(from_location: str, to_location: str, date: str) -> str:
    """
    Backup ground transport search using Kiwi API (RapidAPI).
    Reliable for standard routes (FlixBus, DB, etc.) but less detailed than scraping.
    
    Args:
        from_location: IATA code or city ID (e.g., "LHR", "city:LON").
        to_location: IATA code or city ID (e.g., "PAR", "city:PAR").
        date: Departure date (DD/MM/YYYY).
    """
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{RAPIDAPI_HOST}/search"
    
    querystring = {
        "fly_from": from_location,
        "fly_to": to_location,
        "date_from": date,
        "date_to": date,
        "curr": "USD",
        "sort": "price",
        "limit": "5",
        "vehicle_type": "train,bus" # Key parameter for ground transport
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or not data["data"]:
                return "No ground transport found for the specified criteria."

            results = []
            for trip in data["data"]:
                price = trip.get("price", "N/A")
                currency = data.get("currency", "USD")
                deep_link = trip.get("deep_link", "")
                
                route_info = []
                for leg in trip.get("route", []):
                    # Kiwi uses 'airline' field for bus/train operators too
                    operator = leg.get("airline", "Unknown") 
                    vehicle_type = leg.get("vehicle_type", "unknown")
                    dep_city = leg.get("cityFrom", "Unknown")
                    arr_city = leg.get("cityTo", "Unknown")
                    dep_time = leg.get("local_departure", "")
                    arr_time = leg.get("local_arrival", "")
                    route_info.append(f"[{vehicle_type.upper()}] {operator}: {dep_city} ({dep_time}) -> {arr_city} ({arr_time})")

                results.append(f"Price: {price} {currency}\nRoute: {' | '.join(route_info)}\nLink: {deep_link}\n---")

            return "\n".join(results)

        except Exception as e:
            return f"Error searching ground transport (backup): {str(e)}"

if __name__ == "__main__":
    mcp.run()
