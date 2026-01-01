"""Database configuration and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
from .config import get_settings

settings = get_settings()

# Use DATABASE_URL from env if it's SQLAlchemy-compatible, else fallback to SQLite
# Ignore Prisma-format URLs like "file:./prisma/dev.db"
db_url = settings.database_url
if db_url and not db_url.startswith("file:"):
    DATABASE_URL = db_url
else:
    # Use SQLite for local development (no Docker needed)
    db_path = Path(__file__).parent.parent / "crosswind.db"
    DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


async def init_db():
    """Create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency for FastAPI routes."""
    async with async_session_maker() as session:
        yield session
