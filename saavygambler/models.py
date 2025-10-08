"""Domain models used across SaavyGambler."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional


@dataclass
class TeamStats:
    team_id: str
    name: str
    league: Optional[str] = None
    season: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    points_for: Optional[float] = None
    points_against: Optional[float] = None


@dataclass
class PlayerStats:
    player_id: str
    name: str
    team_id: Optional[str] = None
    position: Optional[str] = None
    games_played: Optional[int] = None
    points_per_game: Optional[float] = None
    rebounds_per_game: Optional[float] = None
    assists_per_game: Optional[float] = None
    custom_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class Event:
    event_id: str
    league_id: Optional[str]
    home_team_id: str
    away_team_id: str
    event_date: date
    venue: Optional[str] = None
    status: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    home_team_name: Optional[str] = None
    away_team_name: Optional[str] = None

    @property
    def is_final(self) -> bool:
        return bool(self.status and self.status.lower() in {"final", "completed"})


@dataclass
class Odds:
    event_id: str
    home_moneyline: Optional[float]
    away_moneyline: Optional[float]
    spread: Optional[float]
    home_spread_odds: Optional[float]
    away_spread_odds: Optional[float]
    total: Optional[float]
    over_odds: Optional[float]
    under_odds: Optional[float]
    last_updated: Optional[datetime] = None


@dataclass
class FantasyProjection:
    player_id: str
    name: str
    projected_points: float
    floor: float
    ceiling: float
    metadata: Dict[str, float] = field(default_factory=dict)


__all__ = [
    "Event",
    "FantasyProjection",
    "Odds",
    "PlayerStats",
    "TeamStats",
]
