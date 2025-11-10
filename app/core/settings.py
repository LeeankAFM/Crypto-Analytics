"""Application settings for the Crypto Analytics FastAPI service."""
from __future__ import annotations

from functools import lru_cache
from typing import Final

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Configuration values for the application."""

    coingecko_api_base: str = Field(
        default="https://pro-api.coingecko.com/api/v3",
        description="Base URL for the CoinGecko API.",
    )
    coingecko_api_key: str = Field(
        default="CG-wxPUJzK3bXPGnPGd3xMhLQ2z",
        description="API key used to authenticate requests against CoinGecko.",
    )
    request_timeout: float = Field(
        default=10.0,
        description="Timeout in seconds for outbound HTTP requests.",
    )

    class Config:
        env_prefix = "CRYPTO_ANALYTICS_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()


settings: Final[Settings] = get_settings()
