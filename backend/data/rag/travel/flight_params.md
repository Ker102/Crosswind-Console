# Flight Search Parameters

When using flight search tools, correctly map user input to these parameters:

## Cabin Class

For the `cabinClass` parameter, use UPPERCASE values:

| User says | Use value |
|-----------|-----------|
| "economy", "coach" | `economy` |
| "premium economy", "premium" | `premium_economy` |
| "business", "business class" | `business` |
| "first", "first class" | `first` |

## Stops / Direct Flights

For filtering by stops:

- `stops=direct` or `stops=0` → Direct flights only
- `stops=1` → Maximum 1 stop
- No stops parameter → All flights

## Sort Options

For the `sortBy` parameter:

| User intent | Use value |
|-------------|-----------|
| "cheapest", "lowest price" | `price_low` |
| "most expensive" | `price_high` |
| "fastest", "shortest" | `fastest` |
| "best", "recommended" | `best` |

## Passengers

- `adults` (required): Number of adult passengers (12+ years)
- `children`: Ages 2-11
- `infants`: Under 2 years (seated on lap)

## Airport/City Codes

For `originSkyId` and `destinationSkyId`:
- Use IATA 3-letter airport codes: `TLL`, `HEL`, `CDG`, `JFK`
- Or use city/entity IDs from the `searchAirport` autocomplete endpoint

Common mappings:
| City | Main Airport | Code |
|------|-------------|------|
| Tallinn | Lennart Meri | TLL |
| Helsinki | Vantaa | HEL |
| Paris | Charles de Gaulle | CDG |
| London | Heathrow | LHR |
| New York | JFK | JFK |
| Stockholm | Arlanda | ARN |
| Riga | Riga | RIX |
| Vilnius | Vilnius | VNO |

## Trip Types

- **One-way**: Use `searchFlights` with departure date only
- **Round-trip**: Use `searchRoundtrip` with both departure and return dates
- **Multi-city**: Use `searchMultiCity` (if available)
