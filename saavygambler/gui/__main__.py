"""Module entry point for ``python -m saavygambler.gui``."""
from __future__ import annotations

from .app import main

__all__ = ["main"]

if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
