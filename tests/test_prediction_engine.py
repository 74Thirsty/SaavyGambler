from datetime import date

from stattrackerpro.models import Event, TeamStats
from stattrackerpro.services.prediction import PredictionEngine


def test_predict_spread_uses_basic_stats():
    engine = PredictionEngine(home_advantage=3.0)
    event = Event(
        event_id="1",
        league_id="123",
        home_team_id="H",
        away_team_id="A",
        event_date=date.today(),
    )
    home = TeamStats(team_id="H", name="Home", points_for=110, points_against=100, wins=20, losses=10)
    away = TeamStats(team_id="A", name="Away", points_for=100, points_against=105, wins=15, losses=15)

    prediction = engine.predict_spread(event, home, away)

    assert prediction.event_id == "1"
    assert prediction.confidence >= 0.5
    assert prediction.spread > 0


def test_predict_moneyline_handles_small_sample():
    engine = PredictionEngine()
    event = Event(
        event_id="1",
        league_id="123",
        home_team_id="H",
        away_team_id="A",
        event_date=date.today(),
    )
    home = TeamStats(team_id="H", name="Home", wins=1, losses=0)
    away = TeamStats(team_id="A", name="Away", wins=0, losses=1)

    prediction = engine.predict_moneyline(event, home, away)
    assert 0 < prediction.home_win_probability < 1
    assert prediction.away_win_probability == 1 - prediction.home_win_probability
