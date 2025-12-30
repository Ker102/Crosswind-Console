"""Autocomplete API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from ..database import get_db
from ..models import Airport, Currency

router = APIRouter(prefix="/api/autocomplete", tags=["autocomplete"])


@router.get("/airports")
async def search_airports(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search airports by city, name, or IATA code.
    
    Returns city groups (e.g., 'Helsinki (any)') for cities with multiple airports,
    followed by individual airport results.
    """
    search = f"%{q.lower()}%"
    
    # Fetch matching airports
    stmt = (
        select(Airport)
        .where(
            or_(
                Airport.city.ilike(search),
                Airport.name.ilike(search),
                Airport.iata.ilike(search),
                Airport.country.ilike(search),
            )
        )
        .order_by(Airport.city)
        .limit(limit * 3)  # Fetch more to group properly
    )
    result = await db.execute(stmt)
    airports = result.scalars().all()
    
    # Extract the base city name from the search query
    # Group airports by (search_term, country) where the city/name contains the search term
    query_lower = q.lower().strip()
    
    # Group airports by country that match the query
    country_groups: dict[str, list[Airport]] = defaultdict(list)
    for airport in airports:
        city_lower = airport.city.lower()
        name_lower = airport.name.lower()
        
        # Check if query matches start of city or is a significant word in the name
        if city_lower.startswith(query_lower) or name_lower.startswith(query_lower):
            country_groups[airport.country].append(airport)
    
    results = []
    
    # Add city-level options for countries with multiple airports matching query
    for country, country_airports in country_groups.items():
        if len(country_airports) >= 2:
            # Use the query as the city hint (capitalize it)
            city_hint = q.strip().title()
            results.append({
                "type": "city",
                "label": f"{city_hint} (any - {len(country_airports)} airports)",
                "value": city_hint,  # Kiwi/Skyscanner accept city names
                "city": city_hint,
                "country": country,
                "airportCount": len(country_airports),
            })
    
    # Add individual airports
    for airport in airports[:limit]:
        results.append({
            "type": "airport",
            **airport.to_dict()
        })
    
    # Sort: city groups first, then airports
    results.sort(key=lambda x: (0 if x["type"] == "city" else 1, x.get("country", "")))
    
    return results[:limit]


@router.get("/currencies")
async def search_currencies(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search currencies by code or name."""
    search = f"%{q.lower()}%"
    stmt = (
        select(Currency)
        .where(
            or_(
                Currency.code.ilike(search),
                Currency.name.ilike(search),
            )
        )
        .limit(limit)
    )
    result = await db.execute(stmt)
    currencies = result.scalars().all()
    return [c.to_dict() for c in currencies]

