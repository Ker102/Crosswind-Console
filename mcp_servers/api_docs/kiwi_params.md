# Kiwi.com Cheap Flights API (RapidAPI Wrapper)

**Base URL**: `https://kiwi-com-cheap-flights.p.rapidapi.com`

## Endpoints

### 1. One-Way Search
**Path**: `/one-way`
**Method**: `GET`

### 2. Round-Trip Search
**Path**: `/round-trip`
**Method**: `GET`

## Parameters (Common)

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `source` | string | Yes | Origin airport code (IATA) | `LHR`, `JFK`, `TLL` |
| `destination` | string | Yes | Destination airport code (IATA) | `CDG`, `HND`, `HEL` |
| `date` | string | Yes | Departure date (YYYY-MM-DD) | `2024-12-10` |
| `returnDate` | string | No | Return date (YYYY-MM-DD) for round-trip | `2024-12-20` |
| `adults` | int | No | Number of adults (default: 1) | `1` |
| `children` | int | No | Number of children (default: 0) | `0` |
| `infants` | int | No | Number of infants (default: 0) | `0` |
| `cabinClass` | string | No | Class: `ECONOMY`, `BUSINESS`, `FIRST_CLASS` | `ECONOMY` |
| `currency` | string | No | Currency code | `USD`, `EUR` |
| `sort` | string | No | Sort by: `price`, `duration`, `quality` | `price` |
| `limit` | int | No | Max results | `10` |

## Notes
- **Location**: Use IATA codes directly (e.g., `TLL`). Do not use `city:` prefix for this wrapper.
- **Date Format**: The standard format is `YYYY-MM-DD`. Some endpoints might accept `DD-MM-YYYY` but `YYYY-MM-DD` is safer.
- **Response**: JSON object with `data` array containing flight details.
