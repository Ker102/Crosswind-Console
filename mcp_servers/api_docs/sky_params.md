# Flights Scraper Sky API (Skyscanner)

**Base URL**: `https://flights-sky.p.rapidapi.com`

## Endpoints

### 1. Auto-Complete (Location Search)
**Path**: `/web/flights/auto-complete`
**Method**: `GET`
**Params**:
- `query` (string): City or airport name (e.g., "Tallinn")

**Response Parsing**:
- Entity ID is located at: `data[0].presentation.id`
- Fallback: `data[0].navigation.entityId`

### 2. One-Way Search
**Path**: `/web/flights/search-one-way`
**Method**: `GET`
**Params**:
- `fromEntityId`: Origin ID (from auto-complete)
- `toEntityId`: Destination ID (from auto-complete)
- `departDate`: YYYY-MM-DD
- `adults`: int
- `cabinClass`: `economy`, `premium_economy`, `business`, `first`

### 3. Round-Trip Search
**Path**: `/web/flights/search-roundtrip`
**Method**: `GET`
**Params**:
- `fromEntityId`, `toEntityId`
- `departDate`: YYYY-MM-DD
- `returnDate`: YYYY-MM-DD

### 4. Incomplete Search (Handling Long-Running Queries)
**Path**: `/web/flights/search-incomplete`
**Method**: `GET`
**Params**:
- `sessionId`: The session ID from the initial search response (if `status` is `incomplete`)
- OR use the original query parameters again, as some APIs treat it as a polling mechanism.
- **Correct Usage**: Check `data.context.status`. If `incomplete`, use `itineraryId` or `token` from response to fetch details?
- **User Instruction**: "In case the status is 'incomplete'(data->context->status=incomplete), you need to use the /flights/search-incomplete endpoint to get the full data until the status is 'complete'"

- Auto-complete is essential to get the `entityId` format (e.g., `eyJ...`).

## Google Flights Endpoints (Backup)
Use these when standard Skyscanner search fails or for price comparison.

### 5. Google One-Way Search
**Path**: `/google/flights/search-one-way`
**Method**: `GET`
**Params**:
- `fromEntityId`, `toEntityId`: (Search IDs)
- `departDate`: YYYY-MM-DD
- `adults`: int
- `cabinClass`: `ECONOMY`, `BUSINESS` (same enum)

### 6. Google Round-Trip Search
**Path**: `/google/flights/search-roundtrip`
**Method**: `GET`
**Params**:
- `fromEntityId`, `toEntityId`
- `departDate`
- `returnDate`

## Booking.com Flights Endpoints (Backup)

### 7. Booking.com One-Way
**Path**: `/booking/flights/search-one-way`
**Method**: `GET`
**Params**:
- `fromEntityId`, `toEntityId`
- `departDate`
- `adults`, `cabinClass`

### 8. Booking.com Round-Trip
**Path**: `/booking/flights/search-roundtrip`
**Method**: `GET`
**Params**:
- `fromEntityId`, `toEntityId`
- `departDate`
- `returnDate`
