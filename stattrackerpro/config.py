"""Application configuration management.

This module intentionally avoids third-party dependencies so that the
package remains lightweight for the kata exercises.  The goal is to mimic
the ergonomics of libraries such as :mod:`pydantic` while keeping the
implementation approachable and fully testable within this repository.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional


ENV_PREFIX = "stattrackerpro_"


def _normalise_env(env: Mapping[str, str]) -> Dict[str, str]:
    """Return a lower-cased copy of environment variables.

    Environment variables are case-insensitive on Windows but not on Linux.
    To deliver a predictable behaviour we treat keys as case-insensitive and
    lower-case them when loading configuration values.
    """

    return {key.lower(): value for key, value in env.items()}


def _load_env_file(path: Path) -> Dict[str, str]:
    """Parse ``key=value`` pairs from a ``.env`` style file.

    The format is intentionally small: empty lines and lines starting with ``#``
    are ignored. Values are stripped of surrounding whitespace but otherwise
    left untouched so users can provide paths or tokens verbatim.
    """

    if not path.exists():
        return {}

    entries: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        entries[key.strip()] = value.strip()
    return entries


def _extract_prefixed(env: Mapping[str, str]) -> Dict[str, str]:
    """Return only entries prefixed with :data:`ENV_PREFIX`."""

    normalised = _normalise_env(env)
    prefix = ENV_PREFIX
    return {key[len(prefix) :]: value for key, value in normalised.items() if key.startswith(prefix)}


@dataclass
class AppSettings:
    """Settings for the StatTrackerPro application.

    The class offers a tiny subset of the conveniences of ``BaseSettings`` from
    Pydantic: values may be provided as constructor arguments or derived from
    environment variables. Type coercion and basic validation keep the
    behaviour predictable for the rest of the code base.
    """

    sportsdb_api_key: str = "1"
    http_timeout_seconds: float = 10.0
    cache_dir: Optional[Path] = None
    _source: Dict[str, str] = field(default_factory=dict, repr=False, init=False)

    def __post_init__(self) -> None:
        if self.http_timeout_seconds <= 0:
            raise ValueError("http_timeout_seconds must be greater than zero")
        if self.cache_dir is not None and not isinstance(self.cache_dir, Path):
            self.cache_dir = Path(self.cache_dir)
        if self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(
        cls,
        env: Optional[Mapping[str, str]] = None,
        *,
        env_file: Iterable[Path] = (Path(".env"),),
    ) -> "AppSettings":
        """Instantiate settings from environment variables.

        Parameters
        ----------
        env:
            Mapping of environment variables to use. When ``None`` the current
            process environment is consulted.
        env_file:
            Optional iterable of ``.env`` files. The first existing file is
            loaded and merged with the live environment, with the live
            environment taking precedence.
        """

        combined: Dict[str, str] = {}
        for path in env_file:
            combined.update(_load_env_file(path))
        if env is None:
            env = os.environ
        combined.update(env)
        scoped = _extract_prefixed(combined)

        data: Dict[str, object] = {}
        if "sportsdb_api_key" in scoped:
            value = str(scoped["sportsdb_api_key"]).strip()
            if value:
                data["sportsdb_api_key"] = value
        if "http_timeout_seconds" in scoped:
            try:
                data["http_timeout_seconds"] = float(scoped["http_timeout_seconds"])
            except ValueError as exc:  # pragma: no cover - defensive programming
                raise ValueError("http_timeout_seconds must be a number") from exc
        if "cache_dir" in scoped:
            data["cache_dir"] = Path(scoped["cache_dir"])

        settings = cls(**data)
        settings._source = dict(scoped)
        return settings


@lru_cache()
def get_settings() -> AppSettings:
    """Return a cached instance of :class:`AppSettings`."""

    return AppSettings.from_env()


__all__ = ["AppSettings", "get_settings"]
