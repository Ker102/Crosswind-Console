Test Endpoint

AppParams(30)Headers(1)BodyAuthorizations

Request URL

rapidapi.com

Query Params

source (optional)

String

Add multiple countries o cities separating by comma:
Country:GB,City:warsaw\_pl,City:berlin\_de

destination (optional)

String

Add multiple cities or countries separating by comma like:
City:dubrovnik\_hr,City:warsaw\_pl,Country:GB

outboundDepartmentDateStart (optional)

String

Date in format:
2023-07-22T00:00:00
use together with outboundDepartmentDateEnd

outboundDepartmentDateEnd (optional)

String

Date in format:
2023-07-22T00:00:00
use together with outboundDepartmentDateStart

currency (optional)

String

locale (optional)

String

adults (optional)

Number

Default: 1

children (optional)

Number

Default: 0

infants (optional)

Number

Default: 0

handbags (optional)

Number

Default: 1

holdbags (optional)

Number

Default: 0

cabinClass (optional)

String

choose one: ECONOMY \| ECONOMY\_PREMIUM \| BUSINESS \| FIRST\_CLASS

sortBy (optional)

String

choose one: POPULARITY \| PRICE

applyMixedClasses (optional)

String

true or false

allowChangeInboundDestination (optional)

String

allowChangeInboundSource (optional)

String

allowDifferentStationConnection (optional)

String

enableSelfTransfer (optional)

String

allowOvernightStopover (optional)

String

enableTrueHiddenCity (optional)

String

allowReturnToDifferentCity (optional)

String

allowReturnFromDifferentCity (optional)

String

enableThrowAwayTicketing (optional)

String

maxStopsCount (optional)

Number

How many stops do you accept?
use number 0, 1 or 2 or leave empty for default

Default: 0

priceStart (optional)

Number

set priceStart and priceEnd to use price range filter correctly.

Default: 0

priceEnd (optional)

Number

set priceStart and priceEnd to use price range filter correctly.

Default: 0

outbound (optional)

String

Which days do you accept for flights?
Separate them by comma like:
SUNDAY,WEDNESDAY,THURSDAY

Only uppercase work

transportTypes (optional)

String

you can use multiple, separating by comma like:
FLIGHT, BUS, TRAIN

contentProviders (optional)

String

limit (optional)

Number

How many results?
Lower amount = faster query

Default: 20

X-RapidAPI-Host \*

AuthorizationNo additional authorizations needed

Code SnippetsExample ResponsesResults

Target:

Shell

Client:

cURL

```shell
curl --request GET
	--url 'https://kiwi-com-cheap-flights.p.rapidapi.com/one-way?source=Country%3AGB&destination=City%3Adubrovnik_hr&currency=usd&locale=en&adults=1&children=0&infants=0&handbags=1&holdbags=0&cabinClass=ECONOMY&sortBy=QUALITY&applyMixedClasses=true&allowChangeInboundDestination=true&allowChangeInboundSource=true&allowDifferentStationConnection=true&enableSelfTransfer=true&allowOvernightStopover=true&enableTrueHiddenCity=true&allowReturnToDifferentCity=false&allowReturnFromDifferentCity=false&enableThrowAwayTicketing=true&outbound=SUNDAY%2CWEDNESDAY%2CTHURSDAY%2CFRIDAY%2CSATURDAY%2CMONDAY%2CTUESDAY&transportTypes=FLIGHT&contentProviders=FLIXBUS_DIRECTS%2CFRESH%2CKAYAK%2CKIWI&limit=20'
	--header 'x-rapidapi-host: kiwi-com-cheap-flights.p.rapidapi.com'
```

reCAPTCHA

Recaptcha requires verification.

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

protected by **reCAPTCHA**

reCAPTCHA is changing its terms of service. [Take action.](https://google.com/recaptcha/admin/migrate)

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

StripeM-Inner