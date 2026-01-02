# Airbnb Search Parameters

Use `search_airbnb` for accommodation searches. Parameters:

## Location
- **locationQueries** (array): List of locations to search
  - Example: `["London", "Manchester", "Birmingham"]`

## Dates (Required for pricing)
- **checkIn** (string): Check-in date in `YYYY-MM-DD` format
  - Example: `2025-07-15`
- **checkOut** (string): Check-out date in `YYYY-MM-DD` format
  - Example: `2025-07-20`

## Guests
| Parameter | Type | Description |
|-----------|------|-------------|
| adults | integer | Number of adults (min: 1) |
| children | integer | Number of children (min: 0) |
| infants | integer | Number of infants (min: 0) |
| pets | integer | Number of pets (min: 0) |

## Price Filters
- **priceMin** (integer): Minimum price per night (default currency)
- **priceMax** (integer): Maximum price per night
- **currency** (string): Currency code for prices
  - Options: `USD`, `EUR`, `GBP`, `CAD`, `AUD`, `JPY`, etc.
  - Default: `USD`

## Property Filters
| Parameter | Type | Description |
|-----------|------|-------------|
| minBeds | integer | Minimum number of beds |
| minBedrooms | integer | Minimum number of bedrooms |
| minBathrooms | integer | Minimum number of bathrooms |

## Locale
- **locale** (string): Language/region for results
  - Default: `en-US`
  - Options: `en-GB`, `de-DE`, `fr-FR`, `es-ES`, `it-IT`, `ja-JP`, etc.

## Example Usage
```
Search for: "2 bedroom apartment in Paris for 4 adults, July 15-20, under $200/night"

Parameters:
- locationQueries: ["Paris"]
- checkIn: "2025-07-15"
- checkOut: "2025-07-20"
- adults: 4
- minBedrooms: 2
- priceMax: 200
- currency: "USD"
```
