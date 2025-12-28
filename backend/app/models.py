"""SQLAlchemy models for autocomplete data."""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Airport(Base):
    """Airport/city data for location autocomplete."""
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)  # "Tallinn Airport"
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # "Tallinn"
    country: Mapped[str] = mapped_column(String(100), nullable=False)  # "Estonia"
    iata: Mapped[str | None] = mapped_column(String(3), index=True)  # "TLL"
    icao: Mapped[str | None] = mapped_column(String(4))  # "EETN"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "iata": self.iata,
            "icao": self.icao,
            "label": f"{self.city}, {self.country}" + (f" ({self.iata})" if self.iata else ""),
            "value": self.iata or self.city,
        }


class Currency(Base):
    """Currency codes for currency autocomplete."""
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)  # "USD"
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # "US Dollar"

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "label": f"{self.code} - {self.name}",
            "value": self.code,
        }
