# Google Maps API Guidance

The Google Maps APIs are self-describing via MCP. Use these tools for location-based queries:

## Available Tools

### 1. `get_directions`
Get route between two locations.
- **origin**: Starting location (address or place name)
- **destination**: End location
- **mode**: `driving`, `walking`, `transit`, `bicycling`

Use when: User asks "how to get from X to Y", "directions to", "route between"

### 2. `geocode_address`
Convert address to coordinates.
- **address**: Address or place name to geocode

Use when: Need lat/lng for other API calls, verify location exists

### 3. `reverse_geocode`
Convert coordinates to address.
- **latitude**: Latitude coordinate
- **longitude**: Longitude coordinate

Use when: Have coordinates, need human-readable address

### 4. `text_search_places`
Search for places using text query.
- **query**: Search text (e.g., "restaurants in Paris")
- **location**: Optional bias location

Use when: "Find restaurants", "search for hotels", "cafes near"

### 5. `search_places_nearby`
Find places near coordinates by type.
- **latitude**: Center latitude
- **longitude**: Center longitude
- **place_type**: Type of place to find
- **radius_meters**: Search radius (default 1500m)

**Place Types:**
- `restaurant`, `cafe`, `bar`
- `hotel`, `lodging`
- `tourist_attraction`, `museum`, `park`
- `hospital`, `pharmacy`
- `gas_station`, `parking`
- `airport`, `train_station`, `bus_station`

## Chaining Example
```
User: "Find Italian restaurants near the Eiffel Tower"

1. geocode_address("Eiffel Tower, Paris") → get lat/lng
2. text_search_places("Italian restaurant", location="Paris")
   OR
   search_places_nearby(lat, lng, "restaurant", 1000)
```

## Error Handling
- If location not found: Suggest user be more specific
- If no results: Expand search radius or try different query
