from datetime import date

from saavygambler.models import Event, Odds, PlayerStats, TeamStats
from saavygambler.providers.base import SportsDataProvider
from saavygambler.services.analytics import AnalyticsService


class StubProvider(SportsDataProvider):
    def __init__(self) -> None:
        self.team = TeamStats(
            team_id="1",
            name="Test Team",
            points_for=110,
            points_against=102,
            wins=20,
            losses=10,
        )

    def search_teams(self, name: str):
        return [self.team]

    def get_team(self, team_id: str):
        return self.team

    def get_events(self, league_id: str, *, from_date=None):
        return [
            Event(
                event_id="E1",
                league_id=league_id,
                home_team_id="1",
                away_team_id="2",
                event_date=date.today(),
            )
        ]

    def lookup_events(self, event_ids):
        return [
            Event(
                event_id=event_ids[0],
                league_id="999",
                home_team_id="1",
                away_team_id="2",
                event_date=date.today(),
            )
        ]

    def get_player_stats(self, player_ids):
        return [
            PlayerStats(
                player_id="P1",
                name="Player 1",
                points_per_game=20,
                assists_per_game=5,
                rebounds_per_game=7,
            )
        ]

    def get_odds(self, event_id: str):
        return Odds(
            event_id=event_id,
            home_moneyline=-150,
            away_moneyline=130,
            spread=-4.5,
            home_spread_odds=-110,
            away_spread_odds=-110,
            total=215.5,
            over_odds=-105,
            under_odds=-115,
        )


def test_insights_and_fantasy_from_stub_provider():
    service = AnalyticsService(StubProvider())

    insights = service.insights_for_league("999")
    assert insights
    assert insights[0].spread_prediction.event_id == "E1"

    projections = service.fantasy_projections(["P1"])
    assert projections
    assert projections[0].player_id == "P1"
