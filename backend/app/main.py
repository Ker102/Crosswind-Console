from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import discovery, llm, autocomplete, mcp_tools
from .schemas import HealthResponse
from .database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(title=settings.project_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"], # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(discovery.router, prefix="/api")
app.include_router(llm.router, prefix="/api")
app.include_router(autocomplete.router)
app.include_router(mcp_tools.router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    status = "ok" if settings.environment == "production" else "degraded" if not settings.enable_mock_data else "ok"
    return HealthResponse(status=status, environment=settings.environment)

