[![RapidAPI Hub: public API Marketplace](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-fe-static.s3.amazonaws.com%2Ftheming%2FRapid_Logo_Primary.png&w=256&q=10)](https://rapidapi.com/hub)

Search APIs

[Add Your API](https://rapidapi.com/auth?referral=/studio) Sign InSign Up

[Discovery](https://rapidapi.com/hub)

Workspace

Sign Up

[![Booking com icon](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2Fca20e4e1-1fe5-4f06-ac3d-e8565b7a735e.png&w=32&q=75)\\
\\
API Overview](https://rapidapi.com/tipsters/api/booking-com)

Version [Open playground](https://rapidapi.com/tipsters/api/booking-com/playground/apiendpoint_ad1960c9-9d82-480b-b0d2-71f28064f8cd)

v1 (current)

Endpoints

MCP Playground

Metadata

[GET\\
\\
Exchange rates](https://rapidapi.com/tipsters/api/booking-com/playground/apiendpoint_ffc82748-b2c1-492a-bc82-bd408ed78d67)

Hotels

Car Rental

Attractions

Flights

V2 Hotels

Static

3. [categories](https://rapidapi.com/categories)
5. [Travel](https://rapidapi.com/search/Travel)
7. [![icon](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2Fca20e4e1-1fe5-4f06-ac3d-e8565b7a735e.png&w=32&q=75)\\
Booking com](https://rapidapi.com/tipsters/api/booking-com)

Test Endpoint

[Overview](https://rapidapi.com/tipsters/api/booking-com) [Tutorials](https://rapidapi.com/tipsters/api/booking-com/tutorials) [Discussions](https://rapidapi.com/tipsters/api/booking-com/discussions)

![Booking com API thumbnail](https://rapidapi.com/hub/_next/image?url=https%3A%2F%2Frapidapi-prod-apis.s3.amazonaws.com%2Fca20e4e1-1fe5-4f06-ac3d-e8565b7a735e.png&w=3840&q=75)

# Booking com

(65)

9.9 Popularity

100% Service Level

581ms Latency

N/A Test

[BASIC\\
\\
$0.00 / mo](https://rapidapi.com/tipsters/api/booking-com/pricing) [PRO\\
\\
$19.00 / mo](https://rapidapi.com/tipsters/api/booking-com/pricing) [ULTRA\\
\\
$49.00 / mo](https://rapidapi.com/tipsters/api/booking-com/pricing) [MEGA\\
\\
$99.00 / mo](https://rapidapi.com/tipsters/api/booking-com/pricing)

[See what subscription plans this API provides.](https://rapidapi.com/tipsters/api/booking-com/pricing)

# Spotlights

[![API Hub Consumer Quick Start Guide](https://rapidapi.com/hub/_next/image?url=%2Fhub%2Fimages%2Fspotlight-default.png&w=3840&q=75)\\
\\
Spotlight\\
\\
API Hub Consumer Quick Start GuideAPI Hub Consumer Quick Start Guide](https://docs.rapidapi.com/docs/consumer-quick-start-guide)

[![Search hotels in Amsterdam](https://cf.bstatic.com/xdata/images/explorer_city/1680x560/28834.jpg?k=c19c2db30abdcd30e246f6b3ba493c0ccfb641b2c7b0c0f309c08612d9235f01&o=)\\
\\
Spotlight\\
\\
Search hotels in AmsterdamGreat savings on hotels in Amsterdam, Netherlands online. Good availability and great rates. Read hotel reviews and choose the best hotel deal for your stay.](https://www.booking.com/city/nl/amsterdam.en-gb.html)

# API Overview

Booking.com is available in 43 languages and offers more than 28 million reported accommodation listings, including over 6.2 million homes, apartments, and other unique places to stay. Wherever you want to go and whatever you want to do, Booking.com makes it easy and supports you with 24/7 customer support.

📬 Support: [tipsters@rapi.one](mailto:tipsters@rapi.one) \| [https://t.me/api\_tipsters](https://t.me/api_tipsters)

✈️ Other Travel API: [https://rapi.one/travel/](https://rapi.one/travel/)

🚀 OpenAPI Specification: [Booking com OpenApi](https://hugeapi.com/collection/booking-com)

Find all hotels, view prices, photos of the hotels, reviews. Find car rental deals. You can make a website like: hotels.com, booking.com, agoda.com

#### Consuming API

**What is RapidAPI?**
RapidAPI is the world’s largest API hub where over three million developers find, test, and connect to thousands of APIs — all with a single account and API key.

**How to start?**

1. Log In or [Sign Up](https://rapidapi.com/auth/sign-up)
2. Subscribing to an API
3. Testing an API from the browser
4. Integrating the API into an application
5. Profit!

[RapidAPI Consumer Quick Start Guide](https://docs.rapidapi.com/docs/consumer-quick-start-guide)

[FAQs - RapidAPI Hub](https://docs.rapidapi.com/docs/faqs)

**This api is free?**
Yes. But there are limits on requests per month.

**I need other limits or a tariff plan**

Support: [tipsters@rapi.one](mailto:tipsters@rapi.one)

* * *

#### How to use Booking API?

##### 0\. Get the possible values

Tutorials -> possible-values

##### 1\. Search locations or hotels by name

Find the required location upon request.

Endpoint: **@Search locations**`/v1/hotels/locations`

Answer:

```
[\
  {\
    "name": "London",\
    "rtl": 0,\
    "timezone": "Europe/London",\
    "dest_type": "city",\
    "landmark_type": -1,\
    "lc": "en",\
    "city_name": "London",\
    "city_ufi": null,\
    "dest_id": "-2601889",\
    "cc1": "gb",\
    "country": "United Kingdom",\
    "label": "London, Greater London, United Kingdom",\
    "image_url": "https://cf.bstatic.com/xdata/images/city/150x150/613094.jpg?k=f751e035ae2c0ac97263ed7d150bae607ffa17a88c55e81cec907941d6bb078b&o=",\
    "longitude": -0.127634,\
    "latitude": 51.507391,\
    "region": "Greater London",\
    "nr_hotels": 14510,\
    "hotels": 14510,\
    "type": "ci"\
  },\
  {\
    "landmark_type": -1,\
    "lc": "en",\
    "rtl": 0,\
    "name": "Central London",\
    "dest_type": "district",\
```\
\
Comparable to:\
![Search locations](https://rapi.one/DOCSMD/book_ln08uhs2/img/n1v4z8t.png)\
\
##### 2\. Search hotels\
\
Get available hotels by the filter. Indicate the `destination_id` and `dest_type` from **@Search locations**, check-in and check-out date, number of adults and children.\
\
For accessible special filters, use: **@Filters for search**`/v1/hotels/search-filters`\
\
Endpoint: **@Search hotels**`v1/hotels/search`\
\
**Use page\_number to paginate and navigate through the result pages**\
\
Answer:\
\
```\
  ],
  "result": [\
    {\
      "id": "property_card_791664",\
      "hotel_name": "Cheval Thorney Court at Hyde Park",\
      "class_is_estimated": 0,\
      "hotel_has_vb_boost": 0,\
      "district": "Kensington and Chelsea",\
      "cant_book": null,\
      "distance_to_cc": "4.00",\
      "mobile_discount_percentage": 0,\
      "is_mobile_deal": 0,\
      "is_free_cancellable": 0,\
      "countrycode": "gb",\
      "latitude": 51.5011118011927,\
      "districts": "1545,29,44,333,2280",\
      "city_name_en": "London",\
      "min_total_price": 379.24,\
      "hotel_id": 791664,\
      ...\
```\
\
Comparable to:\
![Search hotels](https://rapi.one/DOCSMD/book_ln08uhs2/img/pcuk81r.png)\
\
##### 3\. Get all information about hotels and reservations\
\
You got a `hotel_id`. Use it for full hotel information.\
\
Use points:\
\
**@Hotel on the map**\
\
**@Questions about the hotel**\
\
**@Hotel children policy**\
\
**@Reviews of the hotel**\
\
**@Photos of the hotel**\
\
**@Payment features of the hotel**\
\
**@Tips of the hotel**\
\
**@Location highlights of the hotel**\
\
**@Room list of the hotel**\
\
**@Facilities of the hotel**\
\
**@Review scores of the hotel**\
\
**@Reviews metadata of the hotel**\
\
**@Nearby places of the hotel**\
\
**@Description of the hotel**\
\
**@Policies of the hotel**\
\
* * *\
\
#### FAQ\
\
##### How to search for the nearest hotels in the coordinates?\
\
Use Endpoint: **@Search hotels by coordinates**`v1/hotels/search-by-coordinates`\
\
##### Can you please let me know if booking api provide online hotel booking and cancelation features\
\
You can find the hotel and room, then get a link to complete your booking on the booking site.\
\
ex.: [https://secure.booking.com/book.html?hotel\_id=7292334&checkin=2021-09-14&interval=2&stage=1&nr\_rooms\_729233401\_325315371\_3\_0\_0=1](https://secure.booking.com/book.html?hotel_id=7292334&checkin=2021-09-14&interval=2&stage=1&nr_rooms_729233401_325315371_3_0_0=1)\
\
##### Filter by currency does not work, why are prices in a different currency?\
\
Prices and filter are always in the currency of the hotel. Those. if the main payment in the country is in euros, then the price will be in euros. It has always been that way.\
\
# Provider Info\
\
API creator\
\
T\
\
[by Tipsters CO](https://rapidapi.com/user/tipsters)\
\
subscribers\
\
14427\
\
subs\
\
category\
\
Travel\
\
resources\
\
[Product Website](https://rapi.one/travel/)\
\
Sign Up to Contact Provider\
\
get notifications\
\
reCAPTCHA\
\
Recaptcha requires verification.\
\
[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)\
\
protected by **reCAPTCHA**\
\
reCAPTCHA is changing its terms of service. [Take action.](https://google.com/recaptcha/admin/migrate)\
\
[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)\
\
StripeM-Inner