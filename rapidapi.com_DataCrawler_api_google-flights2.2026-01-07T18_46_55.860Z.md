[![RapidAPI Hub: public API Marketplace](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-fe-static.s3.amazonaws.com%2Ftheming%2FRapid_Logo_Primary.png&w=256&q=10)](https://rapidapi.com/hub)

Search APIs

[Add Your API](https://rapidapi.com/auth?referral=/studio) Sign InSign Up

[Discovery](https://rapidapi.com/hub)

Workspace

Sign Up

[![Google Flights icon](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2F1d9e106d-613a-4ca3-9fb2-8315fe73d39c.png&w=32&q=75)\\
\\
API Overview](https://rapidapi.com/DataCrawler/api/google-flights2)

Version [Open playground](https://rapidapi.com/DataCrawler/api/google-flights2/playground/apiendpoint_ce4a44ea-f781-4baf-883f-ea1b7da10907)

v1 (current)

Endpoints

MCP Playground

Meta

[GET\\
\\
Get Available Languages](https://rapidapi.com/DataCrawler/api/google-flights2/playground/apiendpoint_7b54cd51-4588-496c-b037-212a9b2dec68) [GET\\
\\
Get Available Locations](https://rapidapi.com/DataCrawler/api/google-flights2/playground/apiendpoint_2f05c8c0-7880-4d81-9270-416b5cc65c35) [GET\\
\\
Get Available Currencies](https://rapidapi.com/DataCrawler/api/google-flights2/playground/apiendpoint_d4c26742-7413-439d-9d62-b4ef5189ab93) [GET\\
\\
Check Server](https://rapidapi.com/DataCrawler/api/google-flights2/playground/apiendpoint_0f977763-0a07-43ce-93b9-ce7c20b042d4)

Flight

3. [categories](https://rapidapi.com/categories)
5. [Travel](https://rapidapi.com/search/Travel)
7. [![icon](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2F1d9e106d-613a-4ca3-9fb2-8315fe73d39c.png&w=32&q=75)\\
Google Flights](https://rapidapi.com/DataCrawler/api/google-flights2)

Test Endpoint

[Overview](https://rapidapi.com/DataCrawler/api/google-flights2) [Tutorials](https://rapidapi.com/DataCrawler/api/google-flights2/tutorials) [Discussions](https://rapidapi.com/DataCrawler/api/google-flights2/discussions)

![Google Flights API thumbnail](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2F1d9e106d-613a-4ca3-9fb2-8315fe73d39c.png&w=3840&q=75)

# Google Flights

(51)

9.9 Popularity

98% Service Level

8634ms Latency

94% Test

[BASIC\\
\\
$0.00 / mo](https://rapidapi.com/DataCrawler/api/google-flights2/pricing) [PRO\\
\\
$12.99 / mo](https://rapidapi.com/DataCrawler/api/google-flights2/pricing) [ULTRA\\
\\
$35.00 / mo](https://rapidapi.com/DataCrawler/api/google-flights2/pricing) [MEGA\\
\\
⭐️\\
\\
$125.00 / mo](https://rapidapi.com/DataCrawler/api/google-flights2/pricing)

[See what subscription plans this API provides.](https://rapidapi.com/DataCrawler/api/google-flights2/pricing)

# Spotlights

[![Google Flights API: A Step-by-Step Integration Tutorial](https://rapidapi.com/DataCrawler/api/google-flights2)\\
\\
Spotlight\\
\\
Google Flights API: A Step-by-Step Integration TutorialAPI Spotlight](https://extractedge.com/2024/12/29/google-flights-api-a-step-by-step-integration-tutorial/)

![Google Flights API](https://rapidapi.com/DataCrawler/api/google-flights2)

Spotlight

Google Flights APIAPI Spotlight

# API Overview

The Google Flights API is your ultimate solution for accessing real-time flight data and streamlining travel-related services. Whether you’re creating a travel booking app, a flight comparison platform, or enhancing your existing services, this API empowers you with the tools needed to deliver seamless user experiences.

With global coverage and advanced filtering options, you can access up-to-date flight schedules, pricing, and availability. Compare tickets across multiple airlines and find the best deals for domestic and international routes. This API is perfect for startups, travel agencies, and developers looking to integrate flight search capabilities into their platforms.

Why Choose Google Flights API?

- Access real-time flight data for accurate results.
- Compare prices across airlines effortlessly.
- Search flights with filters like date, destination, and airline.
- Boost user engagement with a reliable and fast API.

The Google Flights API provides real-time flight data, ticket prices, and availability to help you build travel platforms, booking apps, or flight comparison tools with ease.

# Google Flights API Documentation

This document provides a detailed overview of the Google Flights API endpoints, including descriptions, required parameters, examples, and their usage. Parameters for each endpoint are organized in tables for better clarity.

## Overview

The Google Flights API enables users to search for flights, retrieve historical price data, and generate insights for better travel planning. Designed for developers, this API simplifies flight searches, provides calendar and grid views, and supports redirection to booking partners.

* * *

## 1\. **Get Supported Currencies**

### Endpoint

- **Path**: `/api/v1/getCurrency`
- **Method**: GET

### Description

Retrieve a list of supported currencies, including their codes, formats, and descriptions.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | None | - | - | - | - |

### Example Request

```http
GET /api/v1/getCurrency
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736172322756,
  "data": [\
    {\
      "currency_code": "KMF",\
      "format": "'KMF' #,##0",\
      "title": "Comorian franc",\
      "subTitle": "Comorian francs"\
    },\
    {\
      "currency_code": "DOP",\
      "format": "'DOP' #,##0",\
      "title": "Dominican peso",\
      "subTitle": "Dominican pesos"\
    }\
  ]
}
```

* * *

## 2\. **Get Supported Locations**

### Endpoint

- **Path**: `/api/v1/getLocations`
- **Method**: GET

### Description

Retrieve a list of supported locations, including country codes and names.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | None | - | - | - | - |

### Example Request

```http
GET /api/v1/getLocations
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736172408665,
  "data": [\
    {\
      "country_code": "AF",\
      "country_name": "Afghanistan"\
    },\
    {\
      "country_code": "AL",\
      "country_name": "Albania"\
    }\
  ]
}
```

* * *

## 3\. **Get Supported Languages**

### Endpoint

- **Path**: `/api/v1/getLanguages`
- **Method**: GET

### Description

Retrieve a list of supported languages and their codes.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | None | - | - | - | - |

### Example Request

```http
GET /api/v1/getLanguages
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736172582262,
  "data": [\
    {\
      "language_code": "af",\
      "title": "Afrikaans"\
    },\
    {\
      "language_code": "bs",\
      "title": "Bosanski"\
    }\
  ]
}
```

* * *

## 4\. **Search Airport**

### Endpoint

- **Path**: `/api/v1/searchAirport`
- **Method**: GET

### Description

Search for airports based on user input.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `query` | Search keyword (e.g., city, state, or airport name). | Yes | - | `Los Angeles` or `LAX` |
| 2. | `language_code` | The preferred language for results. | No | `en-US` | `en-US` |
| 3. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/searchAirport?query=LAX&language_code=en-US&country_code=US
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736172673898,
  "data": [\
    {\
      "id": "LAX",\
      "type": "airport",\
      "title": "Los Angeles International Airport",\
      "subtitle": "International airport in Los Angeles, California",\
      "city": "Los Angeles"\
    },\
    {\
      "id": "/m/023l1x",\
      "type": "other",\
      "title": "Laxey, Isle of Man",\
      "subtitle": "Village in Geography of the Isle of Man",\
      "city": "Laxey"\
    }\
  ]
}
```

* * *

## 5\. **Get Calendar Picker**

### Endpoint

- **Path**: `/api/v1/getCalendarPicker`
- **Method**: GET

### Description

Provides calendar data to display flight prices for a date range.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `departure_id` | IATA code of the departure airport. | Yes | - | `LAX` |
| 2. | `arrival_id` | IATA code of the arrival airport. | Yes | - | `JFK` |
| 3. | `outbound_date` | The departure date. | Yes | - | `2025-04-01` |
| 4. | `start_date` | Start of the calendar range. | No | `Today’s date` | `2025-04-01` |
| 5. | `end_date` | End of the calendar range. | No | `Next month end` | `2025-04-30` |
| 6. | `adults` | Number of adults (12+ years). | No | `1` | `2` |
| 7. | `children` | Number of children (2-11 years). | No | `0` | `1` |
| 8. | `infant_in_seat` | Number of infants requiring a seat. | No | `0` | `1` |
| 9. | `infant_on_lap` | Number of infants without a seat. | No | `0` | `1` |
| 10. | `trip_type` | The `trip_type` parameter specifies the type of journey for the flight search. It determines whether the search is for a one-way trip or a round trip. | No | `ONE_WAY` | `ROUND` |
| 11. | `trip_days` | The `trip_days` parameter specifies the number of days between the outbound and return flights for round-trip searches.. | No | `7` | `6` |
| 12. | `travel_class` | Preferred travel class. | No | `ECONOMY` | `BUSINESS` |
| 13. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 14. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/getCalendarPicker?departure_id=LAX&arrival_id=JFK&outbound_date=2025-04-01
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736172929405,
  "data": [\
    {\
      "departure": "2025-01-06",\
      "price": 1234\
    },\
    {\
      "departure": "2025-01-07",\
      "price": 897\
    }\
  ]
}
```

* * *

## 6\. **Search Flights**

### Endpoint

- **Path**: `/api/v1/searchFlights`
- **Method**: GET

### Description

Search for one-way or round-trip flights based on the given parameters.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `departure_id` | IATA code of the departure airport. | Yes | - | `LAX` |
| 2. | `arrival_id` | IATA code of the arrival airport. | Yes | - | `JFK` |
| 3. | `outbound_date` | The departure date. | Yes | - | `2025-04-01` |
| 4. | `return_date` | The return date for round-trip flights. | No | - | `2025-04-10` |
| 5. | `adults` | Number of adults (12+ years). | No | `1` | `2` |
| 6. | `children` | Number of children (2-11 years). | No | `0` | `1` |
| 7. | `infant_in_seat` | Number of infants requiring a seat. | No | `0` | `1` |
| 8. | `infant_on_lap` | Number of infants without a seat. | No | `0` | `1` |
| 9. | `travel_class` | Preferred travel class. | No | `ECONOMY` | `BUSINESS` |
| 10. | `show_hidden` | The show\_hidden parameter specifies whether to include hidden or restricted flights in the search results. | No | `0` | `1` |
| 11. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 12. | `language_code` | The preferred language for results. | No | `en-US` | `en-US` |
| 13. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/searchFlights?departure_id=LAX&arrival_id=JFK&outbound_date=2025-04-01
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173057440,
  "data": {
    "itineraries": {
      "topFlights": [\
        {\
          "departure_time": "05-04-2025 07:50 AM",\
          "arrival_time": "05-04-2025 10:10 AM",\
          "duration": {"raw": 140, "text": "2 hr 20 min"},\
          "price": 100,\
          "stops": 0\
        }\
      ]
    }
  }
}
```

* * *

## 7\. **Search Multi-City Flights**

### Endpoint

- **Path**: `/api/v1/searchMultiCityFlights`
- **Method**: POST

### Description

Search for multi-city flights, allowing users to book complex itineraries with multiple destinations.

### Body

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `legs` | Array of flight legs with departure and arrival details. | Yes | - | `[{"departure_id":"LAX","arrival_id":"JFK","outbound_date":"2025-04-01"}]` |
| 2. | `adults` | Number of adults (12+ years). | No | `1` | `2` |
| 3. | `children` | Number of children (2-11 years). | No | `0` | `1` |
| 4. | `infant_in_seat` | Number of infants requiring a seat. | No | `0` | `1` |
| 5. | `infant_on_lap` | Number of infants without a seat. | No | `0` | `1` |
| 6. | `travel_class` | Preferred travel class. | No | `ECONOMY` | `BUSINESS` |
| 7. | `show_hidden` | The show\_hidden parameter specifies whether to include hidden or restricted flights in the search results. | No | `0` | `1` |
| 8. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 9. | `language_code` | The preferred language for results. | No | `en-US` | `en-US` |
| 10. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
POST /api/v1/searchMultiCityFlights
```

Body(JSON)

```json
{
  "travel_class": "ECONOMY",
  "adults": 1,
  "children": 0,
  "infant_on_lap": 0,
  "infant_in_seat": 0,
  "show_hidden": 1,
  "currency": "USD",
  "language_code": "en-US",
  "country_code": "US",
  "legs": [\
    {\
      "departure_id": "BOM",\
      "arrival_id": "CCU",\
      "date": "2025-04-07"\
    },\
    {\
      "departure_id": "CCU",\
      "arrival_id": "DEL",\
      "date": "2025-04-14"\
    },\
    {\
      "departure_id": "DEL",\
      "arrival_id": "IXL",\
      "date": "2025-04-21"\
    }\
  ]
}
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173057440,
  "data": {
    "itineraries": [\
      {\
        "legs": [\
          {\
            "departure": "LAX",\
            "arrival": "JFK",\
            "departure_time": "2025-04-01T07:50:00",\
            "arrival_time": "2025-04-01T15:30:00",\
            "price": 450\
          }\
        ]\
      }\
    ]
  }
}
```

* * *

## 8\. **Get Next Flights**

### Endpoint

- **Path**: `/api/v1/getNextFlights`
- **Method**: GET

### Description

Retrieve additional flight results based on the next token provided from a previous search.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `next_token` | Token obtained from the previous flight search. | Yes | - | `abc123` |
| 2. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 3. | `language_code` | The preferred language for results. | No | `en-US` | `en-US` |
| 4. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/getNextFlights?next_token=abc123
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173057440,
  "data": {
    "itineraries": [\
      {\
        "departure_time": "2025-04-01T07:50:00",\
        "arrival_time": "2025-04-01T15:30:00",\
        "price": 420\
      }\
    ]
  }
}
```

* * *

## 9\. **Get Booking Details**

### Endpoint

- **Path**: `/api/v1/getBookingDetails`
- **Method**: GET

### Description

Provides detailed booking information, including partners, prices, and redirection tokens.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `booking_token` | Unique token from flight search results to retrieve booking details. | Yes | - | `xyz123` |
| 2. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 3. | `language_code` | The preferred language for results. | No | `en-US` | `en-US` |
| 4. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/getBookingDetails?booking_token=xyz123
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173354236,
  "data": [\
    {\
      "partner": "Akasa Air",\
      "price": 99,\
      "token": "EsgQCgJRUBoECAMQAUK9BAoCVVMSBWVuLVVT...",\
      "is_airline": true\
    }\
  ]
}
```

* * *

## 10\. **Get Booking URL**

### Endpoint

- **Path**: `/api/v1/getBookingURL`
- **Method**: GET

### Description

Generates a URL for redirecting users to complete their booking on a partner’s website.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `token` | Token obtained from booking details. | Yes | - | `abc123` |

### Example Request

```http
GET /api/v1/getBookingURL?token=abc123
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173354236,
  "data": "https://www.partnerbooking.com?token=abc123"
}
```

* * *

## 11\. **Get Price Graph**

### Endpoint

- **Path**: `/api/v1/getPriceGraph`
- **Method**: GET

### Description

Fetches price data to render a graph showing flight prices over time.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `departure_id` | IATA code of the departure airport. | Yes | - | `LAX` |
| 2. | `arrival_id` | IATA code of the arrival airport. | Yes | - | `JFK` |
| 3. | `outbound_date` | The departure date. | Yes | - | `2025-04-01` |
| 4. | `return_date` | The return date for round-trip flights. | No | - | `2025-04-10` |
| 5. | `start_date` | Start of the calendar range. | No | - | `2025-04-01` |
| 6. | `end_date` | End of the calendar range. | No | - | `2025-04-10` |
| 7. | `adults` | Number of adults (12+ years). | No | `1` | `2` |
| 8. | `children` | Number of children (2-11 years). | No | `0` | `1` |
| 9. | `infant_in_seat` | Number of infants requiring a seat. | No | `0` | `1` |
| 10. | `infant_on_lap` | Number of infants without a seat. | No | `0` | `1` |
| 11. | `travel_class` | Preferred travel class. | No | `ECONOMY` | `BUSINESS` |
| 12. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 13. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/getPriceGraph?departure_id=LAX&arrival_id=JFK&outbound_date=2025-04-01
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173892665,
  "data": [\
    {\
      "departure": "2025-04-01",\
      "price": 622\
    },\
    {\
      "departure": "2025-04-02",\
      "price": 697\
    }\
  ]
}
```

* * *

## 12\. **Get Calendar Grid**

### Endpoint

- **Path**: `/api/v1/getCalendarGrid`
- **Method**: GET

### Description

Fetches a grid view of flight prices for a range of dates to compare departure and return options.

### Query Parameters

| Sr No. | Parameter | Description | Required | Default Value | Example |
| --- | --- | --- | --- | --- | --- |
| 1. | `departure_id` | IATA code of the departure airport. | Yes | - | `LAX` |
| 2. | `arrival_id` | IATA code of the arrival airport. | Yes | - | `JFK` |
| 3. | `outbound_date` | Departure date. | Yes | - | `2025-04-01` |
| 4. | `return_date` | The return date for round-trip flights. | No | - | `2025-04-07` |
| 5. | `start_date_x` | Represents the starting date for the X-axis of the grid view. This axis typically corresponds to outbound travel dates in the calendar grid. | No | - | `2025-04-01` |
| 6. | `end_date_x` | Represents the ending date for the X-axis of the grid view. This axis typically corresponds to outbound travel dates in the calendar grid. | No | - | `2025-04-07` |
| 7. | `start_date_y` | Represents the starting date for the Y-axis of the grid view. This axis typically corresponds to return travel dates in the calendar grid (for round-trip searches). | No | - | `2025-04-01` |
| 8. | `end_date_y` | Represents the ending date for the Y-axis of the grid view. This axis typically corresponds to return travel dates in the calendar grid (for round-trip searches). | No | - | `2025-04-07` |
| 9. | `adults` | Number of adults (12+ years). | No | `1` | `2` |
| 10. | `children` | Number of children (2-11 years). | No | `0` | `1` |
| 11. | `infant_in_seat` | Number of infants requiring a seat. | No | `0` | `1` |
| 12. | `infant_on_lap` | Number of infants without a seat. | No | `0` | `1` |
| 13. | `travel_class` | Preferred travel class. | No | `ECONOMY` | `BUSINESS` |
| 14. | `currency` | Currency code for pricing. | No | `USD` | `EUR` |
| 15. | `country_code` | Filters results by the specified country. | No | `US` | `US` |

### Example Request

```http
GET /api/v1/getCalendarGrid?departure_id=LAX&arrival_id=JFK&outbound_date=2025-05-22
```

### Example Response

```json
{
  "status": true,
  "message": "Success",
  "timestamp": 1736173945456,
  "data": [\
    {\
      "departure": "2025-01-06",\
      "return": "2025-01-07",\
      "price": 2350\
    }\
  ]
}
```

* * *

For further inquiries or support, please contact us at [dc.help@outlook.com](mailto:dc.help@outlook.com).

# Provider Info

API creator

![DataCrawler thumbnail](https://s3.amazonaws.com/rapidapi-prod-user/dccf2178-9083-4bbb-8695-b5f9fa27c43e)

[by DataCrawler](https://rapidapi.com/user/DataCrawler)

subscribers

2292

subs

category

Travel

Sign Up to Contact Provider

get notifications

reCAPTCHA

Recaptcha requires verification.

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

protected by **reCAPTCHA**

reCAPTCHA is changing its terms of service. [Take action.](https://google.com/recaptcha/admin/migrate)

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

StripeM-Inner