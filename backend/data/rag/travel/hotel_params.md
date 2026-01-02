# Hotel Search Parameters

Use hotel search APIs for accommodation queries. Available via Flights Sky and Booking.com APIs.

## Flights Sky Hotels (`/hotels/search`)

### Required Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| entityId | string | Location entity ID from `/hotels/auto-complete` |
| checkin | string | Check-in date `YYYY-MM-DD` |
| checkout | string | Check-out date `YYYY-MM-DD` |

### Optional Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| adults | integer | 1 | Number of adults |
| rooms | integer | 1 | Number of rooms |
| market | string | "US" | Market code (from `/get-config`) |
| locale | string | "en-US" | Locale (from `/get-config`) |
| currency | string | "USD" | Currency (from `/get-config`) |

---

## Booking.com Hotels

### Search by Destination
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| dest_id | number | Yes | Destination ID from location search |
| dest_type | enum | Yes | `city`, `region`, `hotel`, `landmark` |
| checkin_date | string | Yes | Format: `YYYY-MM-DD` |
| checkout_date | string | Yes | Format: `YYYY-MM-DD` |
| adults_number | number | Yes | Number of adults (1-29) |
| room_number | number | Yes | Number of rooms (1-29) |
| filter_by_currency | enum | Yes | Currency code: `USD`, `EUR`, `GBP`, etc. |

### Optional Filters
| Parameter | Type | Description |
|-----------|------|-------------|
| children_number | number | Number of children (1-29) |
| children_ages | string | Comma-separated ages: `5,8,12` |
| order_by | enum | Sort: `popularity`, `price`, `review_score`, `distance` |
| locale | enum | Language: `en-gb`, `de`, `fr`, `es`, etc. |
| include_adjacency | boolean | Include nearby locations if few results |
| categories_filter_ids | string | Filter by star rating, amenities |

### Search by Coordinates
| Parameter | Type | Description |
|-----------|------|-------------|
| latitude | number | -90 to 90 |
| longitude | number | -180 to 180 |
| (+ all optional params above) | | |

## Price Filter Examples
```
# Star rating filter
categories_filter_ids = "class::3,class::4"  # 3-4 star hotels

# Price range filter  
categories_filter_ids = "price::USD-100-200"  # $100-$200/night

# Free cancellation
categories_filter_ids = "free_cancellation::1"
```

## Example Usage
```
User: "4-star hotel in Amsterdam for 2 adults, March 15-18, under €150"

Parameters:
- dest_id: -2140479 (Amsterdam)
- dest_type: "city"
- checkin_date: "2025-03-15"
- checkout_date: "2025-03-18"
- adults_number: 2
- room_number: 1
- filter_by_currency: "EUR"
- categories_filter_ids: "class::4,price::EUR-0-150"
- order_by: "popularity"
```
