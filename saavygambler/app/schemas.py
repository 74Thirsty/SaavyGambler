"""Pydantic schemas for API responses."""
from __future__ import annotations

from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TeamSchema(BaseModel):
    team_id: str
    name: str
    league: Optional[str] = None
    season: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    points_for: Optional[float] = None
    points_against: Optional[float] = None


class EventSchema(BaseModel):
    event_id: str
    league_id: Optional[str] = None
    home_team_id: str
    away_team_id: str
    event_date: date
    venue: Optional[str] = None
    status: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class OddsSchema(BaseModel):
    event_id: str
    home_moneyline: Optional[float] = None
    away_moneyline: Optional[float] = None
    spread: Optional[float] = None
    home_spread_odds: Optional[float] = None
    away_spread_odds: Optional[float] = None
    total: Optional[float] = None
    over_odds: Optional[float] = None
    under_odds: Optional[float] = None
    last_updated: Optional[datetime] = None


class SpreadPredictionSchema(BaseModel):
    event_id: str
    spread: float
    confidence: float


class TotalPredictionSchema(BaseModel):
    event_id: str
    total: float
    confidence: float


class EventInsightsSchema(BaseModel):
    event: EventSchema
    home_team: TeamSchema
    away_team: TeamSchema
    odds: Optional[OddsSchema]
    spread_prediction: SpreadPredictionSchema
    total_prediction: TotalPredictionSchema


class FantasyProjectionSchema(BaseModel):
    player_id: str
    name: str
    projected_points: float
    floor: float
    ceiling: float
    metadata: Dict[str, float] = Field(default_factory=dict)


__all__ = [
    "EventInsightsSchema",
    "FantasyProjectionSchema",
]
