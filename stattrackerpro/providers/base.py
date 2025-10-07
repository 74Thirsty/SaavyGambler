"""Abstract interfaces for sports data providers."""
from __future__ import annotations

import abc
from datetime import date
from typing import Iterable, List, Optional

from ..models import Event, Odds, PlayerStats, TeamStats


class SportsDataProvider(abc.ABC):
    """Interface that concrete provider implementations must follow."""

    @abc.abstractmethod
    def search_teams(self, name: str) -> List[TeamStats]:
        """Search for teams by name."""

    @abc.abstractmethod
    def get_events(self, league_id: str, *, from_date: Optional[date] = None) -> List[Event]:
        """Return upcoming or recent events for a league."""

    @abc.abstractmethod
    def get_team(self, team_id: str) -> Optional[TeamStats]:
        """Return a single team by identifier when supported."""

    @abc.abstractmethod
    def get_player_stats(self, player_ids: Iterable[str]) -> List[PlayerStats]:
        """Return statistics for the given players."""

    @abc.abstractmethod
    def get_odds(self, event_id: str) -> Optional[Odds]:
        """Return betting odds for the specified event, when available."""


__all__ = ["SportsDataProvider"]
