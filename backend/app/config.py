from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables/.env."""

    project_name: str = "Cross-Domain Discovery API"
    environment: str = "development"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-pro"
    firecrawl_api_key: str | None = None
    playwright_browsers_path: str | None = None
    database_url: str | None = None
    nextauth_secret: str | None = None
    nextauth_url: str | None = None
    google_client_id: str | None = None
    google_client_secret: str | None = None
    frontend_origin: str | None = None
    enable_mock_data: bool = True
    
    # MCP Keys
    rapidapi_key: str | None = None
    google_maps_api_key: str | None = None
    google_search_cx: str | None = None
    x_bearer_token: str | None = None
    tripadvisor_api_key: str | None = None
    apify_api_token: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
