"""Seed database with airports and currencies data."""
import asyncio
import httpx
from sqlalchemy import select
from .database import engine, async_session_maker, Base
from .models import Airport, Currency


# Common currencies (ISO 4217)
CURRENCIES = [
    ("USD", "US Dollar"), ("EUR", "Euro"), ("GBP", "British Pound"), ("JPY", "Japanese Yen"),
    ("CHF", "Swiss Franc"), ("CAD", "Canadian Dollar"), ("AUD", "Australian Dollar"),
    ("NZD", "New Zealand Dollar"), ("CNY", "Chinese Yuan"), ("HKD", "Hong Kong Dollar"),
    ("SGD", "Singapore Dollar"), ("SEK", "Swedish Krona"), ("NOK", "Norwegian Krone"),
    ("DKK", "Danish Krone"), ("KRW", "South Korean Won"), ("INR", "Indian Rupee"),
    ("RUB", "Russian Ruble"), ("BRL", "Brazilian Real"), ("ZAR", "South African Rand"),
    ("MXN", "Mexican Peso"), ("PLN", "Polish Zloty"), ("THB", "Thai Baht"),
    ("TRY", "Turkish Lira"), ("ILS", "Israeli Shekel"), ("AED", "UAE Dirham"),
    ("SAR", "Saudi Riyal"), ("PHP", "Philippine Peso"), ("MYR", "Malaysian Ringgit"),
    ("IDR", "Indonesian Rupiah"), ("CZK", "Czech Koruna"), ("HUF", "Hungarian Forint"),
    ("CLP", "Chilean Peso"), ("COP", "Colombian Peso"), ("PEN", "Peruvian Sol"),
    ("ARS", "Argentine Peso"), ("VND", "Vietnamese Dong"), ("EGP", "Egyptian Pound"),
    ("NGN", "Nigerian Naira"), ("PKR", "Pakistani Rupee"), ("BDT", "Bangladeshi Taka"),
    ("KWD", "Kuwaiti Dinar"), ("QAR", "Qatari Riyal"), ("OMR", "Omani Rial"),
    ("BHD", "Bahraini Dinar"), ("JOD", "Jordanian Dinar"), ("LKR", "Sri Lankan Rupee"),
    ("RON", "Romanian Leu"), ("BGN", "Bulgarian Lev"), ("HRK", "Croatian Kuna"),
    ("ISK", "Icelandic Krona"), ("MAD", "Moroccan Dirham"), ("TWD", "Taiwan Dollar"),
]


async def fetch_airports() -> list[dict]:
    """Fetch airport data from open source."""
    url = "https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/master/airports.json"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    
    # Filter to airports with IATA codes (major airports) and valid country (iso)
    airports = []
    for a in data:
        iata = a.get("iata")
        iso = a.get("iso")
        name = a.get("name") or ""
        city = a.get("city") or name or "Unknown"
        
        if iata and len(iata) == 3 and iso and city:
            airports.append({
                "name": name,
                "city": city,
                "country": iso,
                "iata": iata,
                "icao": a.get("icao"),
            })
    return airports


async def seed_currencies(session):
    """Seed currency data."""
    result = await session.execute(select(Currency).limit(1))
    if result.scalar():
        print("Currencies already seeded, skipping...")
        return
    
    for code, name in CURRENCIES:
        session.add(Currency(code=code, name=name))
    await session.commit()
    print(f"Seeded {len(CURRENCIES)} currencies")


async def seed_airports(session):
    """Seed airport data from GitHub."""
    result = await session.execute(select(Airport).limit(1))
    if result.scalar():
        print("Airports already seeded, skipping...")
        return
    
    print("Fetching airport data...")
    airports = await fetch_airports()
    
    for a in airports:
        session.add(Airport(**a))
    await session.commit()
    print(f"Seeded {len(airports)} airports")


async def main():
    """Run seed script."""
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        await seed_currencies(session)
        await seed_airports(session)
    
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
