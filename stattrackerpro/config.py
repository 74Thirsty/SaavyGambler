"""Application configuration management.

This module exposes strongly-typed configuration objects used across the
application. The configuration values can be provided via environment
variables or a `.env` file. Defaults are provided for convenient local
development while keeping production-grade safeguards such as strict type
checking and validation.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class AppSettings(BaseSettings):
    """Settings for the StatTrackerPro application.

    Attributes
    ----------
    sportsdb_api_key:
        API key for TheSportsDB. The public demo key (``1``) is used by default
        for experimentation, but users should supply their own key to unlock
        higher rate limits.
    http_timeout_seconds:
        Default timeout used by HTTP clients when communicating with public
        APIs.
    cache_dir:
        Optional directory where HTTP responses and expensive computations can
        be cached. When set, the directory will be created automatically.
    """

    sportsdb_api_key: str = Field(
        default="1",
        description="API key for TheSportsDB or compatible services.",
    )
    http_timeout_seconds: float = Field(
        default=10.0,
        gt=0,
        description="Timeout in seconds for outbound HTTP requests.",
    )
    cache_dir: Optional[Path] = Field(
        default=None,
        description="Directory used to persist cache entries across sessions.",
    )

    class Config:
        env_prefix = "stattrackerpro_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("cache_dir")
    def _ensure_cache_dir(cls, value: Optional[Path]) -> Optional[Path]:
        if value is not None:
            value.mkdir(parents=True, exist_ok=True)
        return value


@lru_cache()
def get_settings() -> AppSettings:
    """Return a cached instance of :class:`AppSettings`.

    The settings object is cached to avoid re-parsing environment variables in
    performance-sensitive paths such as API request handlers.
    """

    return AppSettings()


__all__ = ["AppSettings", "get_settings"]
