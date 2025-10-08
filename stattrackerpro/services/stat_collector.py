"""Utilities to collect and normalize statistics from providers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

from ..models import Event, PlayerStats, TeamStats
from ..providers.base import SportsDataProvider


@dataclass
class StatCollector:
    """Collects statistics from a :class:`SportsDataProvider`."""

    provider: SportsDataProvider

    def teams(self, name: str) -> List[TeamStats]:
        return self.provider.search_teams(name)

    def team(self, team_id: str) -> Optional[TeamStats]:
        return self.provider.get_team(team_id)

    def events(self, league_id: str, *, from_date: Optional[date] = None) -> List[Event]:
        return self.provider.get_events(league_id, from_date=from_date)

    def lookup_events(self, event_ids: Iterable[str]) -> List[Event]:
        return self.provider.lookup_events(event_ids)

    def player_stats(self, player_ids: Iterable[str]) -> List[PlayerStats]:
        return self.provider.get_player_stats(player_ids)


__all__ = ["StatCollector"]
