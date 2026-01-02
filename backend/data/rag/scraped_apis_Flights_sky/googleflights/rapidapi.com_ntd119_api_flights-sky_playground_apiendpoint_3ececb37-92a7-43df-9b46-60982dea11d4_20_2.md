Test Endpoint

AppParams(6)Headers(2)BodyAuthorizations

Request URL

rapidapi.com

Query Params

token \*

String

- Token
- Required: true
- `token` can be retrieved from **/web/flights/search-roundtrip** or **/web/flights/search-one-way** or **/web/flights/search-multi-city** endpoint (data->token)
- Ex: `eyJhIjoxLCJjIjowLCJpIjowLCJjYyI6ImVjb25vbXkiLCJvIjoiWU1RQSIsImQiOiJZSFoiLCJkMSI6IjIwMjQtMDctMDgifQ==`

itineraryId \*

String

- Itinerary id
- Required: true
- `itineraryId` can be retrieved from **/web/flights/search-roundtrip** or **/web/flights/search-one-way** or **/web/flights/search-multi-city** or **/web/flights/search-incomplete** endpoint (data->itineraries->id)
- Ex: `18395-2407081425--31147-0-18169-2407081705`

market (optional)

String

- `market` can be retrieved from /get-config endpoint(data->market)
- Ex: `US`
- Default value: `US`

locale (optional)

String

- `locale` can be retrieved from /get-config endpoint(data->locale)
- Ex: `en-US`
- Default value: `en-US`

currency (optional)

String

- `currency` can be retrieved from /get-config endpoint(data->currency)
- Ex: `USD`
- Default value: `USD`

cookie (optional)

String

- Use this in case of captcha (403) errors or slow latency.
- For details, refer to the link below.
- [https://rapidapi.com/ntd119/api/flights-sky/tutorials/handling-captcha(403)-errors-or-slow-latency](https://rapidapi.com/ntd119/api/flights-sky/tutorials/handling-captcha(403)-errors-or-slow-latency)

X-RapidAPI-Host \*

AuthorizationNo additional authorizations needed

Code SnippetsExample ResponsesResults

Target:

Shell

Client:

cURL

```shell
curl --request GET
	--url https://flights-sky.p.rapidapi.com/web/flights/details
	--header 'Content-Type: application/json'
	--header 'x-rapidapi-host: flights-sky.p.rapidapi.com'
```

reCAPTCHA

StripeM-Inner