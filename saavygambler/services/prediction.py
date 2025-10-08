"""Prediction utilities for spreads, totals, and outcomes."""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import mean
from typing import Iterable, List, Optional, Sequence

from ..models import Event, Odds, TeamStats

DEFAULT_HOME_ADVANTAGE = 2.5
MIN_SAMPLE_SIZE = 5


def _safe_mean(values: Iterable[Optional[float]], *, default: float) -> float:
    filtered = [value for value in values if value is not None]
    return mean(filtered) if filtered else default


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


@dataclass
class SpreadPrediction:
    event_id: str
    spread: float
    confidence: float


@dataclass
class TotalPrediction:
    event_id: str
    total: float
    confidence: float


@dataclass
class MoneylinePrediction:
    event_id: str
    home_win_probability: float
    away_win_probability: float
    edge_vs_market: Optional[float] = None


class PredictionEngine:
    """Run predictive algorithms using historical statistics."""

    def __init__(self, *, home_advantage: float = DEFAULT_HOME_ADVANTAGE) -> None:
        self.home_advantage = home_advantage

    def predict_spread(
        self,
        event: Event,
        home_team: TeamStats,
        away_team: TeamStats,
        odds: Optional[Odds] = None,
    ) -> SpreadPrediction:
        home_ppg = _safe_mean([home_team.points_for], default=100.0)
        away_ppg = _safe_mean([away_team.points_for], default=100.0)
        defensive_factor = _safe_mean(
            [away_team.points_against, home_team.points_against],
            default=100.0,
        )
        expected_margin = (home_ppg - defensive_factor / 2) - (away_ppg - defensive_factor / 2)
        expected_margin += self.home_advantage
        market_spread = odds.spread if odds else None
        confidence = 0.5
        if market_spread is not None:
            confidence = min(0.95, 0.5 + abs(expected_margin - market_spread) / 20)
        return SpreadPrediction(event_id=event.event_id, spread=expected_margin, confidence=confidence)

    def predict_total(
        self,
        event: Event,
        home_team: TeamStats,
        away_team: TeamStats,
        odds: Optional[Odds] = None,
    ) -> TotalPrediction:
        offensive_mean = _safe_mean([home_team.points_for, away_team.points_for], default=100)
        defensive_mean = _safe_mean([home_team.points_against, away_team.points_against], default=100)
        pace_factor = offensive_mean / defensive_mean if defensive_mean else 1.0
        projected_total = offensive_mean * 2 * pace_factor
        if projected_total <= 0:
            projected_total = 200.0
        market_total = odds.total if odds else None
        confidence = 0.5
        if market_total is not None:
            confidence = min(0.95, 0.5 + abs(projected_total - market_total) / 40)
        return TotalPrediction(event_id=event.event_id, total=projected_total, confidence=confidence)

    def predict_moneyline(
        self,
        event: Event,
        home_team: TeamStats,
        away_team: TeamStats,
        odds: Optional[Odds] = None,
    ) -> MoneylinePrediction:
        home_rating = self._rating_from_record(home_team)
        away_rating = self._rating_from_record(away_team)
        diff = home_rating - away_rating + self.home_advantage
        home_prob = logistic(diff / 10)
        away_prob = 1 - home_prob
        edge = None
        if odds and odds.home_moneyline and odds.away_moneyline:
            market_home_prob = self._prob_from_moneyline(odds.home_moneyline)
            edge = home_prob - market_home_prob
        return MoneylinePrediction(
            event_id=event.event_id,
            home_win_probability=home_prob,
            away_win_probability=away_prob,
            edge_vs_market=edge,
        )

    @staticmethod
    def _rating_from_record(team: TeamStats) -> float:
        wins = team.wins or 0
        losses = team.losses or 0
        games = wins + losses
        if games < MIN_SAMPLE_SIZE:
            return 1500.0  # fallback rating
        win_pct = wins / games
        margin = (team.points_for or 0) - (team.points_against or 0)
        return 1500 + (win_pct - 0.5) * 400 + margin

    @staticmethod
    def _prob_from_moneyline(moneyline: float) -> float:
        if moneyline < 0:
            return (-moneyline) / ((-moneyline) + 100)
        return 100 / (moneyline + 100)


def ensemble_spread(predictions: Sequence[SpreadPrediction]) -> SpreadPrediction:
    event_id = predictions[0].event_id
    weights = [pred.confidence for pred in predictions]
    spreads = [pred.spread for pred in predictions]
    total_weight = sum(weights) or 1.0
    weighted_spread = sum(w * s for w, s in zip(weights, spreads)) / total_weight
    confidence = float(min(0.99, sum(weights) / (len(weights) or 1)))
    return SpreadPrediction(event_id=event_id, spread=weighted_spread, confidence=confidence)


def ensemble_total(predictions: Sequence[TotalPrediction]) -> TotalPrediction:
    event_id = predictions[0].event_id
    weights = [pred.confidence for pred in predictions]
    totals = [pred.total for pred in predictions]
    total_weight = sum(weights) or 1.0
    weighted_total = sum(w * t for w, t in zip(weights, totals)) / total_weight
    confidence = float(min(0.99, sum(weights) / (len(weights) or 1)))
    return TotalPrediction(event_id=event_id, total=weighted_total, confidence=confidence)


__all__ = [
    "MoneylinePrediction",
    "PredictionEngine",
    "SpreadPrediction",
    "TotalPrediction",
    "ensemble_spread",
    "ensemble_total",
]
