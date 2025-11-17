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
    enable_mock_data: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
