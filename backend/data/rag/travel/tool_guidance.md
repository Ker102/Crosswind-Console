# Travel Tool Guidance

Use this document to determine which tool to use for travel-related queries.

## Flight Searches

| User Query Pattern | Tool to Use | Key Parameters |
|-------------------|-------------|----------------|
| "Find flights from X to Y" | `searchFlights` | originSkyId, destinationSkyId, date |
| "Round trip to X" | `searchRoundtrip` | origin, destination, departDate, returnDate |
| "Cheapest day to fly" | `getPriceCalendar` | origin, destination, month |
| "Airport code for X" | `searchAirport` | query |
| "Direct flights only" | `searchFlights` | + `stops=direct` |

## Hotel/Accommodation Searches

| User Query Pattern | Tool to Use | Key Parameters |
|-------------------|-------------|----------------|
| "Hotels in Paris" | `search_hotels` | location, checkIn, checkOut |
| "Airbnb in London" | `search_airbnb` | location, checkIn, checkOut, adults |

## Intent Mapping

When the user says:
- **"cheap"** → Sort by price low, or add price filters
- **"fast"** → Sort by duration/fastest
- **"direct"** → Filter stops=0 or stops=direct
- **"next week"** → Calculate date 7 days from today
- **"next month"** → Use flexible date/calendar endpoint
- **"business class"** → cabinClass=business

## Multi-Tool Scenarios

Some queries require multiple tools:

1. **"Flights to Paris next week"**
   - First: `searchAirport("Paris")` to get city/airport ID
   - Then: `searchFlights` with correct entityId

2. **"Best time to visit Rome"**
   - Use `getPriceCalendar` to find cheapest periods
   - Combine with travel guide knowledge
