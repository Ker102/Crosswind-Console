import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("travel")

# API keys are read at call time in each function to ensure proper loading

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
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "kiwi-com-cheap-flights.p.rapidapi.com"
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
    TRIPADVISOR_API_KEY = os.environ.get("TRIPADVISOR_API_KEY")
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
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
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
async def search_flights_sky(from_location: str, to_location: str, date: str) -> str:
    """
    Search for flights using Flights Sky (Skyscanner) API.
    Use this ALONGSIDE search_flights to compare prices from multiple sources.
    
    Args:
        from_location: Origin city or airport (e.g., "Tallinn", "New York", "TLL").
        to_location: Destination city or airport (e.g., "Helsinki", "Paris", "HEL").
        date: Departure date (YYYY-MM-DD format).
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "flights-sky.p.rapidapi.com"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Step 1: Auto-complete to get entity IDs for origin
            auto_url = "https://flights-sky.p.rapidapi.com/flights/auto-complete"
            
            from_response = await client.get(auto_url, headers=headers, params={"query": from_location})
            from_response.raise_for_status()
            from_data = from_response.json()
            
            from_entity = None
            if from_data.get("data"):
                from_entity = from_data["data"][0].get("id") or from_data["data"][0].get("entityId")
            
            if not from_entity:
                return f"Could not find airport/city for: {from_location}"
            
            # Step 2: Auto-complete for destination
            to_response = await client.get(auto_url, headers=headers, params={"query": to_location})
            to_response.raise_for_status()
            to_data = to_response.json()
            
            to_entity = None
            if to_data.get("data"):
                to_entity = to_data["data"][0].get("id") or to_data["data"][0].get("entityId")
            
            if not to_entity:
                return f"Could not find airport/city for: {to_location}"
            
            # Step 3: Search for flights
            search_url = "https://flights-sky.p.rapidapi.com/flights/search-one-way"
            search_params = {
                "fromEntityId": from_entity,
                "toEntityId": to_entity,
                "departDate": date,
                "adults": "1",
                "currency": "USD",
                "market": "US",
                "locale": "en-US"
            }
            
            search_response = await client.get(search_url, headers=headers, params=search_params)
            search_response.raise_for_status()
            data = search_response.json()
            
            # Parse itineraries
            itineraries = data.get("data", {}).get("itineraries", [])
            if not itineraries:
                return f"No flights found from {from_location} to {to_location} on {date}."
            
            results = []
            for itin in itineraries[:5]:  # Top 5
                price = itin.get("price", {}).get("formatted", "N/A")
                
                legs = itin.get("legs", [])
                if legs:
                    leg = legs[0]
                    origin = leg.get("origin", {}).get("name", from_location)
                    dest = leg.get("destination", {}).get("name", to_location)
                    departure = leg.get("departure", "")[:16].replace("T", " ")
                    arrival = leg.get("arrival", "")[:16].replace("T", " ")
                    duration = leg.get("durationInMinutes", 0)
                    hours, mins = divmod(duration, 60)
                    
                    carriers = leg.get("carriers", {}).get("marketing", [])
                    airline = carriers[0].get("name", "Unknown") if carriers else "Unknown"
                    
                    stops = leg.get("stopCount", 0)
                    stop_text = "Direct" if stops == 0 else f"{stops} stop(s)"
                    
                    results.append(
                        f"✈️ {price} - {airline}\n"
                        f"   {origin} → {dest}\n"
                        f"   Depart: {departure} | Arrive: {arrival}\n"
                        f"   Duration: {hours}h {mins}m | {stop_text}\n---"
                    )
            
            return "\n".join(results) if results else "No flight details available."

        except httpx.HTTPStatusError as e:
            return f"Sky API Error: {e.response.status_code} - {e.response.text[:200]}"
        except Exception as e:
            return f"Error searching Sky flights: {str(e)}"

# Google API keys are read at call time in each function

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
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    GOOGLE_SEARCH_CX = os.environ.get("GOOGLE_SEARCH_CX")
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
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "kiwi-com-cheap-flights.p.rapidapi.com"
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

@mcp.tool()
async def get_directions(origin: str, destination: str, mode: str = "driving") -> str:
    """
    Get directions and route information between two locations using Google Directions API.
    Useful for finding routes from airports to hotels, attractions, or any point of interest.
    
    Args:
        origin: Starting location (e.g., "Malta International Airport", "35.8575,14.4775").
        destination: End location (e.g., "Mdina, Malta", "Blue Grotto Malta").
        mode: Travel mode - 'driving', 'walking', 'bicycling', or 'transit'.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": GOOGLE_API_KEY,
        "alternatives": "true"  # Get multiple route options
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                return f"Error: {data.get('status')} - {data.get('error_message', 'No routes found')}"
            
            results = []
            for i, route in enumerate(data.get("routes", [])[:3]):  # Max 3 routes
                leg = route["legs"][0]  # First leg (direct route)
                
                distance = leg.get("distance", {}).get("text", "Unknown")
                duration = leg.get("duration", {}).get("text", "Unknown")
                start_address = leg.get("start_address", origin)
                end_address = leg.get("end_address", destination)
                
                # Get step-by-step directions (summary)
                steps = []
                for step in leg.get("steps", [])[:5]:  # First 5 steps
                    instruction = step.get("html_instructions", "")
                    # Remove HTML tags
                    instruction = instruction.replace("<b>", "").replace("</b>", "")
                    instruction = instruction.replace("<div>", " ").replace("</div>", "")
                    step_dist = step.get("distance", {}).get("text", "")
                    steps.append(f"  • {instruction} ({step_dist})")
                
                route_summary = route.get("summary", "Main route")
                results.append(
                    f"Route {i+1}: {route_summary}\n"
                    f"From: {start_address}\n"
                    f"To: {end_address}\n"
                    f"Distance: {distance} | Duration: {duration} ({mode})\n"
                    f"Directions:\n" + "\n".join(steps) + "\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error getting directions: {str(e)}"

@mcp.tool()
async def geocode_address(address: str) -> str:
    """
    Convert a street address or place name to geographic coordinates (latitude/longitude).
    
    Args:
        address: The address or place name to geocode (e.g., "1600 Amphitheatre Parkway, Mountain View, CA").
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                return f"Geocoding failed: {data.get('status')} - {data.get('error_message', 'No results found')}"
            
            result = data["results"][0]
            location = result["geometry"]["location"]
            formatted = result["formatted_address"]
            place_id = result.get("place_id", "")
            
            return (
                f"Address: {formatted}\n"
                f"Latitude: {location['lat']}\n"
                f"Longitude: {location['lng']}\n"
                f"Place ID: {place_id}"
            )
        except Exception as e:
            return f"Error geocoding address: {str(e)}"

@mcp.tool()
async def reverse_geocode(latitude: float, longitude: float) -> str:
    """
    Convert geographic coordinates (latitude/longitude) to a human-readable address.
    
    Args:
        latitude: The latitude coordinate.
        longitude: The longitude coordinate.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                return f"Reverse geocoding failed: {data.get('status')}"
            
            results = []
            for i, result in enumerate(data["results"][:3]):  # Top 3 results
                formatted = result["formatted_address"]
                types = ", ".join(result.get("types", [])[:3])
                results.append(f"{i+1}. {formatted} (Type: {types})")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error reverse geocoding: {str(e)}"

@mcp.tool()
async def text_search_places(query: str, location: str = None) -> str:
    """
    Search for places using a text query. Great for finding restaurants, attractions, or any POI.
    
    Args:
        query: Text query like "Best pizza in Rome" or "Museums near Eiffel Tower".
        location: Optional location to bias results (e.g., "Paris, France" or "48.8566,2.3522").
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    # Using the Places API Text Search endpoint
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }
    
    if location:
        # Check if location is already lat,lng format
        if "," in location and all(part.replace(".", "").replace("-", "").isdigit() for part in location.split(",")):
            params["location"] = location
            params["radius"] = 50000  # 50km radius
        else:
            # It's a text location, add to query
            params["query"] = f"{query} near {location}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") not in ["OK", "ZERO_RESULTS"]:
                return f"Places search failed: {data.get('status')} - {data.get('error_message', '')}"
            
            if not data.get("results"):
                return "No places found for your search."
            
            results = []
            for place in data["results"][:5]:  # Top 5 results
                name = place.get("name", "Unknown")
                address = place.get("formatted_address", "No address")
                rating = place.get("rating", "N/A")
                user_ratings = place.get("user_ratings_total", 0)
                types = ", ".join(place.get("types", [])[:3])
                open_now = place.get("opening_hours", {}).get("open_now")
                open_status = "Open now" if open_now else ("Closed" if open_now is False else "Hours unknown")
                
                results.append(
                    f"📍 {name}\n"
                    f"   Address: {address}\n"
                    f"   Rating: {rating}⭐ ({user_ratings} reviews)\n"
                    f"   Type: {types}\n"
                    f"   Status: {open_status}\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching places: {str(e)}"

@mcp.tool()
async def search_places_nearby(latitude: float, longitude: float, place_type: str, radius_meters: int = 1500) -> str:
    """
    Find places near a specific location by type. Use after getting coordinates from geocode_address.
    
    Args:
        latitude: Center point latitude.
        longitude: Center point longitude.
        place_type: Type of place (restaurant, cafe, hotel, museum, tourist_attraction, bar, pharmacy, hospital, etc).
        radius_meters: Search radius in meters (default 1500, max 50000).
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": min(radius_meters, 50000),
        "type": place_type,
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") not in ["OK", "ZERO_RESULTS"]:
                return f"Nearby search failed: {data.get('status')}"
            
            if not data.get("results"):
                return f"No {place_type}s found within {radius_meters}m."
            
            results = []
            for place in data["results"][:7]:  # Top 7 results
                name = place.get("name", "Unknown")
                vicinity = place.get("vicinity", "No address")
                rating = place.get("rating", "N/A")
                user_ratings = place.get("user_ratings_total", 0)
                open_now = place.get("opening_hours", {}).get("open_now")
                open_status = "🟢 Open" if open_now else ("🔴 Closed" if open_now is False else "")
                
                results.append(
                    f"📍 {name} {open_status}\n"
                    f"   {vicinity}\n"
                    f"   Rating: {rating}⭐ ({user_ratings} reviews)\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching nearby: {str(e)}"

if __name__ == "__main__":
    mcp.run()
