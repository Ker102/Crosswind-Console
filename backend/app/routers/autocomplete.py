"""Autocomplete API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Airport, Currency

router = APIRouter(prefix="/api/autocomplete", tags=["autocomplete"])


@router.get("/airports")
async def search_airports(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search airports by city, name, or IATA code."""
    search = f"%{q.lower()}%"
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
        .limit(limit)
    )
    result = await db.execute(stmt)
    airports = result.scalars().all()
    return [a.to_dict() for a in airports]


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
