"""High-level service that orchestrates data collection and predictions."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

from ..models import Event, FantasyProjection, Odds, PlayerStats, TeamStats
from ..providers.base import SportsDataProvider
from .fantasy import FantasyProjector
from .prediction import PredictionEngine, SpreadPrediction, TotalPrediction, ensemble_spread, ensemble_total
from .stat_collector import StatCollector


@dataclass
class EventInsights:
    event: Event
    home_team: TeamStats
    away_team: TeamStats
    odds: Optional[Odds]
    spread_prediction: SpreadPrediction
    total_prediction: TotalPrediction


class AnalyticsService:
    """Provide insights by combining collectors, predictors, and fantasy tools."""

    def __init__(self, provider: SportsDataProvider) -> None:
        self.collector = StatCollector(provider)
        self.predictor = PredictionEngine()
        self.fantasy_projector = FantasyProjector()
        self.provider = provider

    def insights_for_league(self, league_id: str, *, from_date: Optional[date] = None) -> List[EventInsights]:
        events = self.collector.events(league_id, from_date=from_date)
        insights: List[EventInsights] = []
        for event in events:
            home_team = self.collector.team(event.home_team_id) or self._fallback_team(event.home_team_id, "Home")
            away_team = self.collector.team(event.away_team_id) or self._fallback_team(event.away_team_id, "Away")
            odds = self.provider.get_odds(event.event_id)
            spread = self.predictor.predict_spread(event, home_team, away_team, odds)
            total = self.predictor.predict_total(event, home_team, away_team, odds)
            insights.append(
                EventInsights(
                    event=event,
                    home_team=home_team,
                    away_team=away_team,
                    odds=odds,
                    spread_prediction=spread,
                    total_prediction=total,
                )
            )
        return insights

    def fantasy_projections(self, player_ids: Iterable[str]) -> List[FantasyProjection]:
        stats: List[PlayerStats] = self.collector.player_stats(player_ids)
        return self.fantasy_projector.project(stats)

    def lookup_events(self, event_ids: Iterable[str]) -> List[Event]:
        return self.collector.lookup_events(event_ids)

    @staticmethod
    def combine_spread_predictions(predictions: Iterable[SpreadPrediction]) -> SpreadPrediction:
        return ensemble_spread(list(predictions))

    @staticmethod
    def combine_total_predictions(predictions: Iterable[TotalPrediction]) -> TotalPrediction:
        return ensemble_total(list(predictions))

    @staticmethod
    def _fallback_team(team_id: str, label: str) -> TeamStats:
        return TeamStats(team_id=team_id, name=f"Unknown {label}")


__all__ = ["AnalyticsService", "EventInsights"]
