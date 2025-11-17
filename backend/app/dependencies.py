from __future__ import annotations

from functools import lru_cache

from .config import Settings, get_settings
from .services.llm import GeminiClient


@lru_cache
def get_llm_client() -> GeminiClient:
    settings = get_settings()
    return GeminiClient(settings)


def get_app_settings() -> Settings:
    return get_settings()
