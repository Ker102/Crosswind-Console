# Flights Sky API (Skyscanner) - Complete Parameter Reference

**API Host**: `flights-sky.p.rapidapi.com`
**Base URL**: `https://flights-sky.p.rapidapi.com`

---

## 1. Auto-Complete (Get Entity IDs)

**Endpoint**: `GET /flights/auto-complete`

Get the entity IDs needed for flight searches.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | ✅ | City or airport name (e.g., "New York", "Paris") |

### Response Parsing
- Entity ID: `data[0].presentation.id` or `data[0].navigation.entityId`
- Example: `NYCA` for New York (Any), `PARI` for Paris (Any)

---

## 2. One-Way Flight Search

**Endpoint**: `GET /flights/search-one-way`

Search for one-way flights.

### Required Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `fromEntityId` | string | ✅ | Origin location ID | `NYCA`, `TLL`, `PARI` |
| `toEntityId` | string | ✅ | Destination location ID | `MSYA`, `HEL`, `CDG` |
| `departDate` | string | ✅ | Departure date | `2025-01-20` |

### Optional Parameters

| Parameter | Type | Default | Description | Values |
|-----------|------|---------|-------------|--------|
| `adults` | int | 1 | Adult passengers (12+) | 1-9 |
| `children` | int | 0 | Child passengers (2-12) | 0-8 |
| `infants` | int | 0 | Infant passengers (<2) | 0-4 |
| `cabinClass` | string | `economy` | Cabin class | `economy`, `premium_economy`, `business`, `first` |
| `stops` | string | all | Filter by stops | `direct`, `1stop`, `direct,1stop` |
| `market` | string | `US` | Market/country code | `US`, `UK`, `DE` |
| `locale` | string | `en-US` | Language/locale | `en-US`, `en-GB`, `de-DE` |
| `currency` | string | `USD` | Currency code | `USD`, `EUR`, `GBP` |
| `wholeMonthDepart` | string | - | Search entire month | `2025-01` |

---

## 3. Round-Trip Flight Search

**Endpoint**: `GET /flights/search-roundtrip`

Search for round-trip flights.

### Required Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fromEntityId` | string | ✅ | Origin location ID |
| `toEntityId` | string | ✅ | Destination location ID |
| `departDate` | string | ✅ | Departure date (YYYY-MM-DD) |
| `returnDate` | string | ✅ | Return date (YYYY-MM-DD) |

### Optional Parameters
Same as One-Way Search (adults, children, cabinClass, stops, etc.)

---

## 4. Incomplete Search (Polling)

**Endpoint**: `GET /flights/search-incomplete`

When initial search returns `status: incomplete`, poll this endpoint.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sessionId` | string | ✅ | Session ID from initial search response |

### Usage
1. Check `data.context.status` in response
2. If `incomplete`, extract `sessionId` and call this endpoint
3. Repeat until `status` is `complete`

---

## Response Structure

### Itineraries Array
```json
{
  "data": {
    "itineraries": [
      {
        "id": "itinerary-id",
        "price": {
          "raw": 150.00,
          "formatted": "$150"
        },
        "legs": [
          {
            "origin": { "name": "New York JFK" },
            "destination": { "name": "Paris CDG" },
            "durationInMinutes": 480,
            "stopCount": 0,
            "departure": "2025-01-20T10:00:00",
            "arrival": "2025-01-20T22:00:00",
            "carriers": { "marketing": [{ "name": "Delta" }] }
          }
        ]
      }
    ],
    "context": {
      "status": "complete",
      "sessionId": "abc123"
    }
  }
}
```

---

## Common Entity ID Examples

| Location | Entity ID |
|----------|-----------|
| New York (Any) | `NYCA` |
| Paris (Any) | `PARI` |
| London (Any) | `LOND` |
| Los Angeles | `LAXA` |
| Tokyo | `TYOA` |
| Tallinn | `TLL` |
| Helsinki | `HEL` |
| Stockholm | `ARN` |

**Note**: IATA codes (3-letter) often work as entity IDs directly.

---

## Error Handling

- **Empty data**: API returned but no `data` field → Try different entity IDs
- **Timeout**: API took too long → Retry or use Kiwi fallback
- **Status incomplete**: Poll `/search-incomplete` with sessionId
