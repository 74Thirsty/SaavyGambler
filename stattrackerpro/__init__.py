"""StatTrackerPro package initialization."""
from __future__ import annotations

from importlib import import_module
from typing import Any

from .config import AppSettings, get_settings
from .services.analytics import AnalyticsService

__all__ = ["AnalyticsService", "AppSettings", "TheSportsDBProvider", "get_settings"]

_provider_import_error: Exception | None = None

try:  # pragma: no cover - exercised implicitly via optional import paths
    _module = import_module(".providers.thesportsdb", package=__name__)
    TheSportsDBProvider = getattr(_module, "TheSportsDBProvider")
except ModuleNotFoundError as exc:  # pragma: no cover - depends on optional deps
    _provider_import_error = exc
    TheSportsDBProvider = None  # type: ignore[assignment]


def __getattr__(name: str) -> Any:  # pragma: no cover - trivial delegation
    if name == "TheSportsDBProvider" and _provider_import_error is not None:
        raise ModuleNotFoundError(
            "Optional dependency 'httpx' is required to use TheSportsDBProvider",
        ) from _provider_import_error
    raise AttributeError(name)
