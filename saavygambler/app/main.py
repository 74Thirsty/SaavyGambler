"""FastAPI application exposing SaavyGambler functionality."""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query

from ..providers.thesportsdb import TheSportsDBProvider
from ..services.analytics import AnalyticsService, EventInsights
from .schemas import EventInsightsSchema, FantasyProjectionSchema

app = FastAPI(title="SaavyGambler", version="1.0.0")


def get_analytics_service() -> AnalyticsService:
    provider = TheSportsDBProvider()
    return AnalyticsService(provider)


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/leagues/{league_id}/insights", response_model=List[EventInsightsSchema])
def league_insights(
    league_id: str,
    from_date: Optional[date] = Query(None, description="Only include events on or after this date"),
    service: AnalyticsService = Depends(get_analytics_service),
) -> List[EventInsightsSchema]:
    try:
        insights = service.insights_for_league(league_id, from_date=from_date)
        return [EventInsightsSchema.parse_obj(_serialize_insight(insight)) for insight in insights]
    except Exception as exc:  # pragma: no cover - network errors bubble up
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/fantasy/projections", response_model=List[FantasyProjectionSchema])
def fantasy_projections(
    player_ids: List[str],
    service: AnalyticsService = Depends(get_analytics_service),
) -> List[FantasyProjectionSchema]:
    if not player_ids:
        raise HTTPException(status_code=400, detail="player_ids cannot be empty")
    try:
        projections = service.fantasy_projections(player_ids)
        return [FantasyProjectionSchema.parse_obj(projection.__dict__) for projection in projections]
    except Exception as exc:  # pragma: no cover - network errors bubble up
        raise HTTPException(status_code=502, detail=str(exc)) from exc


def _serialize_insight(insight: EventInsights) -> dict:
    return {
        "event": insight.event.__dict__,
        "home_team": insight.home_team.__dict__,
        "away_team": insight.away_team.__dict__,
        "odds": insight.odds.__dict__ if insight.odds else None,
        "spread_prediction": insight.spread_prediction.__dict__,
        "total_prediction": insight.total_prediction.__dict__,
    }
