# Flights Sky API Configuration

This document is auto-generated from the `/get-config` endpoint.

## Tool Usage Guidance

When the user asks about:
- **Flight prices, bookings, or air travel** → Use `searchFlights` or `searchRoundtrip`
- **Airport lookups or codes** → Use `searchAirport` 
- **Price calendars or flexible dates** → Use `getPriceCalendar`

## Valid Market Codes

Use these 2-letter codes for the `market` parameter. Common examples:

| Code | Country |
|------|---------|
| EE | Estonia |
| FI | Finland |
| US | United States |
| GB | United Kingdom |
| DE | Germany |
| FR | France |
| SE | Sweden |
| NO | Norway |
| LV | Latvia |
| LT | Lithuania |
| PL | Poland |
| ES | Spain |
| IT | Italy |
| NL | Netherlands |

> **Full list available via `/get-config` endpoint**

## Valid Currencies

Use these 3-letter ISO codes for the `currency` parameter:

| Code | Name | Symbol |
|------|------|--------|
| EUR | Euro | € |
| USD | US Dollar | $ |
| GBP | British Pound | £ |
| SEK | Swedish Krona | kr |
| NOK | Norwegian Krone | kr |
| DKK | Danish Krone | kr |
| PLN | Polish Zloty | zł |
| CHF | Swiss Franc | CHF |
| JPY | Japanese Yen | ¥ |
| AUD | Australian Dollar | $ |
| CAD | Canadian Dollar | $ |

## Valid Locales

Common locales for the `locale` parameter:

`en-US`, `en-GB`, `de-DE`, `fr-FR`, `es-ES`, `it-IT`, `nl-NL`, `pl-PL`, `sv-SE`, `fi-FI`, `nb-NO`, `da-DK`, `ja-JP`, `zh-CN`, `pt-BR`

## Date Formats

- Dates must be in **YYYY-MM-DD** format
- Example: `2026-01-15` for January 15, 2026
- For "next week", calculate from current date and use YYYY-MM-DD
