Test Endpoint

AppParams(15)Headers(1)BodyAuthorizations

Request URL

rapidapi.com

Query Params

filter\_by\_currency \*

AED

Enum

dest\_id \*

Number

Destination id, use `Search locations` to find a place, field `dest_id` and `dest_type`

Default: -553173

page\_number (optional)

Number

Page number

Default: 0

Minimum: 0

Maximum: 100000

include\_adjacency (optional)

true

Boolean

Include nearby places. If there are few hotels in the selected location, nearby locations will be added. You should pay attention to the `primary_count` parameter - it is the number of hotels from the beginning of the array that matches the strict filter.

children\_number (optional)

Number

Number of children

Default: 2

Minimum: 1

Maximum: 29

room\_number \*

Number

Number of rooms

Default: 1

Minimum: 1

Maximum: 29

categories\_filter\_ids (optional)

String

Search filter IDs. For possible filters use `@Filters for search` ex: `price::USD-140-190`, or `price::USD-150-min` or `price::USD-150-max`

children\_ages (optional)

String

The age of every child. If children will be staying in the room, please indicate their ages separated by commas. 0-less than a year

adults\_number \*

Number

Number of adults

Default: 2

Minimum: 1

Maximum: 29

locale \*

en-gb

Enum

order\_by \*

popularity

Enum

checkin\_date \*

String

Checkin date

units \*

metric

Enum

checkout\_date \*

String

Checkout date

dest\_type \*

city

Enum

X-RapidAPI-Host \*

AuthorizationNo additional authorizations needed

Code SnippetsExample ResponsesResults

Target:

Shell

Client:

cURL

```shell
curl --request GET
	--url 'https://booking-com.p.rapidapi.com/v2/hotels/search-filters?filter_by_currency=AED&dest_id=-553173&page_number=0&include_adjacency=true&children_number=2&room_number=1&categories_filter_ids=class%3A%3A2%2Cclass%3A%3A4%2Cfree_cancellation%3A%3A1&children_ages=5%2C0&adults_number=2&locale=en-gb&order_by=popularity&checkin_date=2026-01-31&units=metric&checkout_date=2026-02-01&dest_type=city'
	--header 'x-rapidapi-host: booking-com.p.rapidapi.com'
```

reCAPTCHA

Recaptcha requires verification.

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

protected by **reCAPTCHA**

reCAPTCHA is changing its terms of service. [Take action.](https://google.com/recaptcha/admin/migrate)

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

StripeM-Inner