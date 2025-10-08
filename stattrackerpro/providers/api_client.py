"""HTTP client utilities for interacting with external data providers."""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from ..config import get_settings

LOGGER = logging.getLogger(__name__)


@dataclass
class CachedResponse:
    """Represents a cached HTTP response."""

    status_code: int
    headers: Dict[str, str]
    data: Any
    timestamp: float
    expires_in: Optional[float] = None

    def is_valid(self) -> bool:
        if self.expires_in is None:
            return True
        return (time.time() - self.timestamp) < self.expires_in


class APIClient:
    """Robust HTTP client with caching and error handling.

    The client exposes a :py:meth:`get_json` helper that retrieves JSON
    responses while honoring configurable timeouts, retry strategies, and an
    optional in-memory cache. This makes it well-suited for production-grade
    integrations with public sports APIs that may enforce rate limits.
    """

    def __init__(self, *, timeout: Optional[float] = None) -> None:
        settings = get_settings()
        self._timeout = timeout or settings.http_timeout_seconds
        self._cache: Dict[str, CachedResponse] = {}
        self._client = httpx.Client(timeout=self._timeout)

    def close(self) -> None:
        self._client.close()

    def get_json(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cache_ttl: Optional[float] = None,
        max_retries: int = 2,
        backoff_factor: float = 0.5,
    ) -> Any:
        """Perform a GET request and return the parsed JSON body.

        Retries transient failures with exponential backoff. When ``cache_ttl``
        is provided, the response is cached for the specified duration in
        seconds.
        """

        cache_key = self._cache_key(url, params)
        if cache_ttl:
            cached = self._cache.get(cache_key)
            if cached and cached.is_valid():
                return cached.data

        attempt = 0
        while True:
            try:
                response = self._client.get(url, params=params, headers=headers)
                if response.status_code == 404:
                    LOGGER.warning("[APIClient] 404 Not Found for %s", response.url)
                    return {}
                response.raise_for_status()
                data = response.json()
                if cache_ttl:
                    self._cache[cache_key] = CachedResponse(
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        data=data,
                        timestamp=time.time(),
                        expires_in=cache_ttl,
                    )
                return data
            except httpx.HTTPStatusError as exc:  # pragma: no cover - network
                LOGGER.error("Request failed with status %s: %s", exc.response.status_code, exc)
                raise
            except httpx.RequestError as exc:
                if attempt >= max_retries:
                    LOGGER.error("Max retries exceeded for %s: %s", url, exc)
                    raise
                sleep_time = backoff_factor * (2**attempt)
                LOGGER.warning(
                    "Request error for %s (attempt %s/%s), retrying in %.2fs",
                    url,
                    attempt + 1,
                    max_retries,
                    sleep_time,
                )
                time.sleep(sleep_time)
                attempt += 1

    def _cache_key(self, url: str, params: Optional[Dict[str, Any]]) -> str:
        key = url
        if params:
            key += json.dumps(params, sort_keys=True)
        return key


__all__ = ["APIClient", "CachedResponse"]
