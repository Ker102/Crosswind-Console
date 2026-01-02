Test Endpoint

AppParams(15)Headers(1)BodyAuthorizations

Request URL

rapidapi.com

Query Params

page\_number (optional)

Number

Page number

Default: 0

Minimum: 0

Maximum: 100000

locale \*

en-gb

Enum

children\_number (optional)

Number

Number of children

Default: 2

Minimum: 1

Maximum: 29

checkout\_date \*

String

Checkout date

checkin\_date \*

String

Checkin date

adults\_number \*

Number

Number of adults

Default: 2

Minimum: 1

Maximum: 29

units \*

metric

Enum

latitude \*

Number

Latitude

Default: 65.9667

Minimum: -90

Maximum: 90

room\_number \*

Number

Number of rooms

Default: 1

Minimum: 1

Maximum: 29

order\_by \*

popularity

Enum

include\_adjacency (optional)

true

Boolean

Include nearby places. If there are few hotels in the selected location, nearby locations will be added. You should pay attention to the `primary_count` parameter - it is the number of hotels from the beginning of the array that matches the strict filter.

longitude \*

Number

Longitude

Default: -18.5333

Minimum: -180

Maximum: 180

categories\_filter\_ids (optional)

String

Search filter IDs. For possible filters use `@Filters for search`

children\_ages (optional)

String

The age of every child. If children will be staying in the room, please indicate their ages separated by commas. 0-less than a year

filter\_by\_currency \*

AED

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
	--url 'https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates?page_number=0&locale=en-gb&children_number=2&checkout_date=2026-02-01&checkin_date=2026-01-31&adults_number=2&units=metric&latitude=65.9667&room_number=1&order_by=popularity&include_adjacency=true&longitude=-18.5333&categories_filter_ids=class%3A%3A2%2Cclass%3A%3A4%2Cfree_cancellation%3A%3A1&children_ages=5%2C0&filter_by_currency=AED'
	--header 'x-rapidapi-host: booking-com.p.rapidapi.com'
```

reCAPTCHA

Recaptcha requires verification.

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

protected by **reCAPTCHA**

reCAPTCHA is changing its terms of service. [Take action.](https://google.com/recaptcha/admin/migrate)

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

StripeM-Inner