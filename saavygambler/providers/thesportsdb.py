"""Implementation of :class:`SportsDataProvider` using TheSportsDB."""
from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, List, Optional

from ..config import get_settings
from ..models import Event, Odds, PlayerStats, TeamStats
from .api_client import APIClient
from .base import SportsDataProvider

BASE_URL = "https://www.thesportsdb.com/api/v1/json"


class TheSportsDBProvider(SportsDataProvider):
    """Fetch data from TheSportsDB public API."""

    def __init__(self, *, client: Optional[APIClient] = None) -> None:
        self._settings = get_settings()
        self._client = client or APIClient()

    @property
    def _base_url(self) -> str:
        return f"{BASE_URL}/{self._resolve_api_key()}"

    def _resolve_api_key(self) -> str:
        value = getattr(self._settings, "sportsdb_api_key", None)
        if value is None:
            return "1"
        key = str(value).strip()
        return key or "1"

    def search_teams(self, name: str) -> List[TeamStats]:
        payload = self._client.get_json(
            f"{self._base_url}/searchteams.php",
            params={"t": name},
            cache_ttl=3600,
        )
        teams = []
        for item in payload.get("teams", []) or []:
            teams.append(
                TeamStats(
                    team_id=item.get("idTeam", ""),
                    name=item.get("strTeam", ""),
                    league=item.get("strLeague"),
                    season=item.get("strSeason"),
                    wins=self._safe_int(item.get("intWins")),
                    losses=self._safe_int(item.get("intLosses")),
                    points_for=self._safe_float(item.get("intPointsFor")),
                    points_against=self._safe_float(item.get("intPointsAgainst")),
                )
            )
        return teams

    def get_events(self, league_id: str, *, from_date: Optional[date] = None) -> List[Event]:
        params = {"id": league_id}
        if from_date:
            params["d"] = from_date.strftime("%Y-%m-%d")
        payload = self._client.get_json(
            f"{self._base_url}/eventsnextleague.php",
            params=params,
            cache_ttl=600,
        )
        events = []
        for item in payload.get("events", []) or []:
            events.append(self._build_event(item))
        return events

    def lookup_events(self, event_ids: Iterable[str]) -> List[Event]:
        events: List[Event] = []
        for event_id in event_ids:
            payload = self._client.get_json(
                f"{self._base_url}/lookupevent.php",
                params={"id": event_id},
                cache_ttl=600,
            )
            for item in payload.get("events", []) or []:
                events.append(self._build_event(item))
        return events

    def get_team(self, team_id: str) -> Optional[TeamStats]:
        payload = self._client.get_json(
            f"{self._base_url}/lookupteam.php",
            params={"id": team_id},
            cache_ttl=3600,
        )
        teams = payload.get("teams", []) or []
        if not teams:
            return None
        team = teams[0]
        return TeamStats(
            team_id=team.get("idTeam", ""),
            name=team.get("strTeam", ""),
            league=team.get("strLeague"),
            season=team.get("strSeason"),
            wins=self._safe_int(team.get("intWins")),
            losses=self._safe_int(team.get("intLosses")),
            points_for=self._safe_float(team.get("intPointsFor")),
            points_against=self._safe_float(team.get("intPointsAgainst")),
        )

    def get_player_stats(self, player_ids: Iterable[str]) -> List[PlayerStats]:
        stats: List[PlayerStats] = []
        for player_id in player_ids:
            payload = self._client.get_json(
                f"{self._base_url}/lookupplayer.php",
                params={"id": player_id},
                cache_ttl=3600,
            )
            for item in payload.get("players", []) or []:
                stats.append(
                    PlayerStats(
                        player_id=item.get("idPlayer", ""),
                        name=item.get("strPlayer", ""),
                        team_id=item.get("idTeam"),
                        position=item.get("strPosition"),
                        games_played=self._safe_int(item.get("intGamesPlayed")),
                        points_per_game=self._safe_float(item.get("strPointsPG")),
                        rebounds_per_game=self._safe_float(item.get("strReboundsPG")),
                        assists_per_game=self._safe_float(item.get("strAssistsPG")),
                    )
                )
        return stats

    def get_odds(self, event_id: str) -> Optional[Odds]:
        payload = self._client.get_json(
            f"{self._base_url}/lookupeventodds.php",
            params={"id": event_id},
            cache_ttl=300,
        )
        odds_list = payload.get("odds", []) or []
        if not odds_list:
            return None
        market = odds_list[0]
        return Odds(
            event_id=event_id,
            home_moneyline=self._safe_float(market.get("homeWinOdds")),
            away_moneyline=self._safe_float(market.get("awayWinOdds")),
            spread=self._safe_float(market.get("pointSpread")),
            home_spread_odds=self._safe_float(market.get("homeSpreadOdds")),
            away_spread_odds=self._safe_float(market.get("awaySpreadOdds")),
            total=self._safe_float(market.get("total")),
            over_odds=self._safe_float(market.get("overOdds")),
            under_odds=self._safe_float(market.get("underOdds")),
        )

    @staticmethod
    def _safe_int(value: Optional[str]) -> Optional[int]:
        try:
            return int(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _safe_float(value: Optional[str]) -> Optional[float]:
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    def _build_event(self, item: dict) -> Event:
        event_date = self._parse_event_date(item.get("dateEvent"))
        return Event(
            event_id=item.get("idEvent", ""),
            league_id=item.get("idLeague"),
            home_team_id=item.get("idHomeTeam", ""),
            away_team_id=item.get("idAwayTeam", ""),
            event_date=event_date,
            venue=item.get("strVenue"),
            status=item.get("strStatus"),
            home_score=self._safe_int(item.get("intHomeScore")),
            away_score=self._safe_int(item.get("intAwayScore")),
            home_team_name=item.get("strHomeTeam"),
            away_team_name=item.get("strAwayTeam"),
        )

    @staticmethod
    def _parse_event_date(value: Optional[str]) -> date:
        if not value:
            return date.today()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return date.today()


__all__ = ["TheSportsDBProvider"]
