# Google Flights2 API Parameters - Complete Guide

The `search_flights_sky` tool uses the Google Flights2 API (google-flights2.p.rapidapi.com).
Use this guide to correctly format all parameters.

---

## Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from_location` | string | Origin IATA airport code | `LHR`, `JFK`, `TLL` |
| `to_location` | string | Destination IATA airport code | `CDG`, `NRT`, `HEL` |
| `date` | string | Departure date in YYYY-MM-DD format | `2026-04-20` |

---

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `return_date` | string | - | Return date for round-trips (YYYY-MM-DD) |
| `adults` | int | 1 | Adult passengers (12+ years) |
| `cabin_class` | string | `economy` | See cabin class values below |
| `max_stops` | int | null | 0=direct only, 1=max 1 stop, 2=max 2 stops |

---

## Cabin Class Values

When the user mentions cabin class, map to these values:

| User Says | Value to Use |
|-----------|--------------|
| "economy", "coach" | `economy` |
| "premium economy", "premium" | `premium_economy` |
| "business", "business class" | `business` |
| "first", "first class" | `first` |

The API internally maps these to `ECONOMY`, `PREMIUM_ECONOMY`, `BUSINESS`, `FIRST`.

---

## Trip Type Handling

| Trip Type | How to Call |
|-----------|-------------|
| One-way | Set `date`, leave `return_date` empty |
| Round-trip | Set both `date` and `return_date` |

---

## Stops / Direct Flights

| User Request | `max_stops` Value |
|--------------|-------------------|
| "direct flights only" | `0` |
| "1 stop maximum" | `1` |
| "up to 2 stops" | `2` |
| "any number of stops" | Leave as `null` |

---

## Common Airport IATA Codes

| City | Airport | IATA Code |
|------|---------|-----------|
| Tallinn | Lennart Meri | `TLL` |
| Helsinki | Vantaa | `HEL` |
| Paris | Charles de Gaulle | `CDG` |
| Paris | Orly | `ORY` |
| London | Heathrow | `LHR` |
| London | Gatwick | `LGW` |
| New York | JFK | `JFK` |
| New York | Newark | `EWR` |
| Los Angeles | LAX | `LAX` |
| Tokyo | Narita | `NRT` |
| Tokyo | Haneda | `HND` |
| Dubai | Dubai | `DXB` |
| Amsterdam | Schiphol | `AMS` |
| Frankfurt | Frankfurt | `FRA` |
| Singapore | Changi | `SIN` |

---

## Response Structure

The API returns flight results in this structure:

```json
{
  "status": true,
  "data": {
    "itineraries": {
      "topFlights": [
        {
          "price": 433,
          "departure_time": "20-04-2026 07:50 AM",
          "arrival_time": "20-04-2026 04:05 PM",
          "duration": {"text": "8 hr 5 min"},
          "stops": 0
        }
      ]
    }
  }
}
```

### Key Fields in Response

| Field | Description |
|-------|-------------|
| `price` | Price in USD (integer) |
| `departure_time` | Formatted departure time |
| `arrival_time` | Formatted arrival time |
| `duration.text` | Human-readable flight duration |
| `stops` | Number of stops (0 = direct) |

---

## Example Usage

### One-way Search
```python
search_flights_sky(
    from_location="LHR",
    to_location="JFK",
    date="2026-04-20",
    adults=1,
    cabin_class="economy"
)
```

### Round-trip Search
```python
search_flights_sky(
    from_location="TLL",
    to_location="CDG",
    date="2026-04-20",
    return_date="2026-04-27",
    adults=2,
    cabin_class="business"
)
```

### Direct Flights Only
```python
search_flights_sky(
    from_location="LAX",
    to_location="NRT",
    date="2026-05-01",
    max_stops=0
)
```

---

## Important Notes

1. **Date Format**: Always use `YYYY-MM-DD` format (e.g., `2026-04-20`)
2. **IATA Codes**: Use 3-letter airport codes, not city names
3. **Autocomplete**: If user provides city name, help them identify the correct IATA code
4. **Currency**: Results are in USD by default
5. **Response Time**: API typically responds in 5-15 seconds
