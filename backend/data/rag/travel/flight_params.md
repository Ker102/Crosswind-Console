# Flight Search Parameters - Complete Guide

When using flight search tools, correctly map user input to these parameters.

---

## Flights Sky API (Skyscanner)

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `fromEntityId` | string | Origin location ID | `NYCA`, `TLL`, `PARI` |
| `toEntityId` | string | Destination location ID | `HEL`, `CDG`, `MSYA` |
| `departDate` | string | Departure date in YYYY-MM-DD | `2025-01-20` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `returnDate` | string | - | Return date for round-trips |
| `adults` | int | 1 | Adult passengers (12+ years) |
| `children` | int | 0 | Child passengers (2-12 years) |
| `infants` | int | 0 | Infant passengers (under 2) |
| `cabinClass` | string | `economy` | See cabin class values below |
| `stops` | string | all | `direct`, `1stop`, or comma-separated |
| `market` | string | `US` | Country code |
| `locale` | string | `en-US` | Language locale |
| `currency` | string | `USD` | Currency code |

---

## Kiwi API (Fallback)

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fly_from` | string | Origin IATA code (e.g., `TLL`) |
| `fly_to` | string | Destination IATA code (e.g., `HEL`) |
| `dateFrom` | string | Departure date DD/MM/YYYY |
| `dateTo` | string | Same as dateFrom for specific date |

### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `return_from` | string | Return date DD/MM/YYYY |
| `return_to` | string | Return date range end |
| `adults` | int | Number of adults |
| `children` | int | Number of children |
| `infants` | int | Number of infants |
| `selected_cabins` | string | `M` (economy), `W` (premium), `C` (business), `F` (first) |
| `max_stopovers` | int | 0 for direct, 1 for max 1 stop |

---

## Cabin Class Mapping

| User Says | Flights Sky Value | Kiwi Value |
|-----------|-------------------|------------|
| "economy", "coach" | `economy` | `M` |
| "premium economy", "premium" | `premium_economy` | `W` |
| "business", "business class" | `business` | `C` |
| "first", "first class" | `first` | `F` |

---

## Stops / Direct Flights

### Flights Sky API
- `stops=direct` → Direct flights only
- `stops=1stop` → Maximum 1 stop
- `stops=direct,1stop` → Direct or 1 stop
- No parameter → All flights

### Kiwi API
- `max_stopovers=0` → Direct flights only
- `max_stopovers=1` → Maximum 1 stop
- `max_stopovers=2` → Maximum 2 stops

---

## Common Airport/Entity IDs

| City | Airport | IATA/Entity ID |
|------|---------|----------------|
| Tallinn | Lennart Meri | `TLL` |
| Helsinki | Vantaa | `HEL` |
| Paris | Charles de Gaulle | `CDG` |
| London | Heathrow | `LHR` |
| New York | Any | `NYCA` |
| New York | JFK | `JFK` |
| Stockholm | Arlanda | `ARN` |
| Riga | Riga | `RIX` |
| Vilnius | Vilnius | `VNO` |
| Amsterdam | Schiphol | `AMS` |
| Frankfurt | Frankfurt | `FRA` |
| Dubai | Dubai | `DXB` |

---

## Trip Type Selection

| Trip Type | Flights Sky Endpoint | Date Parameters |
|-----------|---------------------|-----------------|
| One-way | `/flights/search-one-way` | `departDate` only |
| Round-trip | `/flights/search-roundtrip` | `departDate` + `returnDate` |
| Whole month | `/flights/search-one-way` | `wholeMonthDepart` (YYYY-MM) |

---

## Response Handling

### Price Extraction
- Flights Sky: `itinerary.price.raw` (number) or `itinerary.price.formatted` (string)
- Kiwi: `flight.price` (number in selected currency)

### Direct Flight Info (Kiwi)
- Check `response.DirectFlightsInfo.count` for number of direct options
- Check `flight.route.length` - if 1, it's direct

### Stops Count
- Flights Sky: `leg.stopCount`
- Kiwi: `sector.sectorSegments.length - 1`
