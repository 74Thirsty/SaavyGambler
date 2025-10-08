"""Controller utilities used by the SaavyGambler GUI."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

from ..models import Event, PlayerStats, TeamStats
from ..providers.base import SportsDataProvider
from ..providers.thesportsdb import TheSportsDBProvider
from ..services.stat_collector import StatCollector


@dataclass
class SummaryRow:
    """Lightweight representation of information to display in the UI."""

    title: str
    subtitle: Optional[str] = None


def _format_record(wins: Optional[int], losses: Optional[int]) -> Optional[str]:
    if wins is None and losses is None:
        return None
    if wins is None:
        return f"Losses: {losses}"
    if losses is None:
        return f"Wins: {wins}"
    return f"Record: {wins}-{losses}"


def _format_points(points_for: Optional[float], points_against: Optional[float]) -> Optional[str]:
    if points_for is None and points_against is None:
        return None
    if points_for is None:
        return f"Against: {points_against:.1f}"
    if points_against is None:
        return f"For: {points_for:.1f}"
    return f"For/Against: {points_for:.1f}/{points_against:.1f}"


def _format_event_header(event: Event) -> str:
    home = event.home_team_name or event.home_team_id or "Home"
    away = event.away_team_name or event.away_team_id or "Away"
    return f"{away} at {home}"


def _format_event_status(event: Event) -> Optional[str]:
    if event.home_score is not None and event.away_score is not None:
        return f"Score: {event.away_score}-{event.home_score}"
    if event.status:
        return f"Status: {event.status.title()}"
    return None


def format_team_summary(team: TeamStats) -> SummaryRow:
    """Return a concise summary for display in the UI."""

    title = team.name or f"Team {team.team_id}" or "Unknown Team"
    details: List[str] = []
    if team.league:
        details.append(team.league)
    if team.season:
        details.append(f"Season {team.season}")
    record = _format_record(team.wins, team.losses)
    if record:
        details.append(record)
    points = _format_points(team.points_for, team.points_against)
    if points:
        details.append(points)
    subtitle = " • ".join(details) if details else None
    return SummaryRow(title=title, subtitle=subtitle)


def format_event_summary(event: Event) -> SummaryRow:
    title = _format_event_header(event)
    details: List[str] = []
    if isinstance(event.event_date, date):
        details.append(event.event_date.strftime("%b %d, %Y"))
    status = _format_event_status(event)
    if status:
        details.append(status)
    if event.venue:
        details.append(event.venue)
    subtitle = " • ".join(details) if details else None
    return SummaryRow(title=title, subtitle=subtitle)


def format_player_summary(player: PlayerStats) -> SummaryRow:
    title = player.name or f"Player {player.player_id}" or "Unknown Player"
    details: List[str] = []
    if player.position:
        details.append(player.position)
    if player.team_id:
        details.append(f"Team {player.team_id}")
    metrics: List[str] = []
    if player.points_per_game is not None:
        metrics.append(f"PTS {player.points_per_game:.1f}")
    if player.rebounds_per_game is not None:
        metrics.append(f"REB {player.rebounds_per_game:.1f}")
    if player.assists_per_game is not None:
        metrics.append(f"AST {player.assists_per_game:.1f}")
    for key, value in player.custom_metrics.items():
        metrics.append(f"{key.upper()} {value:.1f}")
    if metrics:
        details.append(", ".join(metrics))
    subtitle = " • ".join(details) if details else None
    return SummaryRow(title=title, subtitle=subtitle)


class StatTrackerController:
    """High level orchestrator used by the graphical interface."""

    def __init__(self, provider: Optional[SportsDataProvider] = None) -> None:
        self._provider = provider or TheSportsDBProvider()
        self._collector = StatCollector(provider=self._provider)

    def search_teams(self, query: str) -> List[TeamStats]:
        return self._collector.teams(query)

    def lookup_events(self, event_ids: Iterable[str]) -> List[Event]:
        return self._collector.lookup_events(event_ids)

    def get_player_stats(self, player_ids: Iterable[str]) -> List[PlayerStats]:
        return self._collector.player_stats(player_ids)


__all__ = [
    "StatTrackerController",
    "SummaryRow",
    "format_event_summary",
    "format_player_summary",
    "format_team_summary",
]
