# Amadeus Flight Offers API - Parameter Guide

The `search_amadeus_flights` tool uses the official Amadeus Flight Offers API.
This is the highest quality flight data source. Use IATA codes only.

---

## Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from_location` | string | Origin IATA airport code | `LHR`, `JFK`, `CDG` |
| `to_location` | string | Destination IATA airport code | `NRT`, `SIN`, `DXB` |
| `date` | string | Departure date YYYY-MM-DD | `2026-04-20` |

---

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `return_date` | string | null | Return date for round-trip (YYYY-MM-DD) |
| `adults` | int | 1 | Number of adult passengers (max 9) |
| `cabin_class` | string | ECONOMY | See cabin class values below |
| `max_results` | int | 10 | Results to return (max 250) |
| `non_stop` | bool | false | If true, only direct flights |

---

## Cabin Class Values

| User Says | Value to Use |
|-----------|--------------|
| "economy", "coach" | `ECONOMY` |
| "premium economy" | `PREMIUM_ECONOMY` |
| "business class" | `BUSINESS` |
| "first class" | `FIRST` |

---

## Trip Type

| Trip Type | How to Call |
|-----------|-------------|
| One-way | Set `date` only, leave `return_date` empty |
| Round-trip | Set both `date` and `return_date` |

---

## Direct Flights

Set `non_stop=true` to only return direct flights without layovers.

---

## Common Airport IATA Codes

| City | Airport | IATA |
|------|---------|------|
| London | Heathrow | LHR |
| London | Gatwick | LGW |
| New York | JFK | JFK |
| New York | Newark | EWR |
| Paris | Charles de Gaulle | CDG |
| Tokyo | Narita | NRT |
| Tokyo | Haneda | HND |
| Dubai | Dubai | DXB |
| Singapore | Changi | SIN |
| Los Angeles | LAX | LAX |
| Sydney | Kingsford Smith | SYD |
| Frankfurt | Frankfurt | FRA |
| Amsterdam | Schiphol | AMS |

---

## Response Format

Returns formatted flight results:
```
🛫 Amadeus Flights: LHR → JFK on 2026-04-20
One-way
------------------------------------------------------------
✈️ USD 417.83 | SWISS INTERNATIONAL AIR LINES | 06:00 → 12:50 | 11h 50m | 1 stop
✈️ USD 445.00 | BRITISH AIRWAYS | 09:30 → 12:45 | 8h 15m | Direct
```

---

## Example Usage

### One-way Economy
```python
search_amadeus_flights(
    from_location="LHR",
    to_location="JFK",
    date="2026-04-20"
)
```

### Round-trip Business Class
```python
search_amadeus_flights(
    from_location="CDG",
    to_location="NRT",
    date="2026-05-01",
    return_date="2026-05-15",
    cabin_class="BUSINESS",
    adults=2
)
```

### Direct Flights Only
```python
search_amadeus_flights(
    from_location="LAX",
    to_location="SYD",
    date="2026-06-01",
    non_stop=True
)
```

---

## Important Notes

1. **IATA Codes Only**: Use 3-letter airport codes, not city names
2. **Date Format**: Always YYYY-MM-DD
3. **Test Environment**: Currently using Amadeus test sandbox (limited routes)
4. **Best For**: Official airline data, accurate pricing, reliable availability
5. **Compare With**: Use alongside `search_flights_sky` and `search_flights` for price comparison

---

# Amadeus Hotel Search API

The `search_amadeus_hotels` tool uses the official Amadeus Hotel List + Hotel Search v3 APIs.

---

## Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `city_code` | string | IATA city code | `PAR`, `LON`, `NYC` |
| `check_in_date` | string | Check-in date YYYY-MM-DD | `2026-04-20` |
| `check_out_date` | string | Check-out date YYYY-MM-DD | `2026-04-25` |

---

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `adults` | int | 1 | Number of adult guests |
| `rooms` | int | 1 | Number of rooms |
| `ratings` | string | null | Comma-separated star ratings (e.g., "4,5") |
| `amenities` | string | null | See amenities list below |
| `max_results` | int | 10 | Max hotels to return |

---

## Amenities Values

| User Says | Value to Use |
|-----------|--------------|
| "spa" | `SPA` |
| "gym", "fitness" | `FITNESS_CENTER` |
| "parking" | `PARKING` |
| "restaurant" | `RESTAURANT` |
| "wifi" | `WIFI` |
| "pool" | `SWIMMING_POOL` |

---

## Common City Codes

| City | Code |
|------|------|
| Paris | PAR |
| London | LON |
| New York | NYC |
| Tokyo | TYO |
| Dubai | DXB |
| Amsterdam | AMS |
| Rome | ROM |

---

## Example Usage

### Basic Hotel Search
```python
search_amadeus_hotels(
    city_code="PAR",
    check_in_date="2026-04-20",
    check_out_date="2026-04-25"
)
```

### Luxury Hotels Only
```python
search_amadeus_hotels(
    city_code="LON",
    check_in_date="2026-05-01",
    check_out_date="2026-05-05",
    ratings="4,5",
    adults=2
)
```

### Hotels with Amenities
```python
search_amadeus_hotels(
    city_code="NYC",
    check_in_date="2026-06-01",
    check_out_date="2026-06-07",
    amenities="spa,pool,gym"
)
```
