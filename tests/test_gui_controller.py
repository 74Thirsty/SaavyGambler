from datetime import date

from stattrackerpro.gui.controller import (
    SummaryRow,
    format_event_summary,
    format_player_summary,
    format_team_summary,
)
from stattrackerpro.models import Event, PlayerStats, TeamStats


def test_format_team_summary_includes_record_and_points():
    team = TeamStats(
        team_id="134876",
        name="Boston Celtics",
        league="NBA",
        season="2024",
        wins=10,
        losses=2,
        points_for=115.4,
        points_against=104.2,
    )

    summary = format_team_summary(team)

    assert isinstance(summary, SummaryRow)
    assert summary.title == "Boston Celtics"
    assert "Record: 10-2" in (summary.subtitle or "")
    assert "For/Against: 115.4/104.2" in (summary.subtitle or "")


def test_format_event_summary_with_scores():
    event = Event(
        event_id="2052711",
        league_id="4328",
        home_team_id="133604",
        away_team_id="133602",
        event_date=date(2024, 4, 12),
        venue="Staples Center",
        status="Final",
        home_score=102,
        away_score=98,
        home_team_name="Los Angeles Lakers",
        away_team_name="Golden State Warriors",
    )

    summary = format_event_summary(event)

    assert summary.title == "Golden State Warriors at Los Angeles Lakers"
    assert "Apr 12, 2024" in (summary.subtitle or "")
    assert "Score: 98-102" in (summary.subtitle or "")


def test_format_player_summary_with_multiple_metrics():
    player = PlayerStats(
        player_id="34145937",
        name="Stephen Curry",
        team_id="GSW",
        position="PG",
        points_per_game=29.8,
        rebounds_per_game=6.1,
        assists_per_game=6.6,
        custom_metrics={"ts": 0.67},
    )

    summary = format_player_summary(player)

    assert summary.title == "Stephen Curry"
    subtitle = summary.subtitle or ""
    assert "PG" in subtitle and "Team GSW" in subtitle
    assert "PTS 29.8" in subtitle
    assert "REB 6.1" in subtitle
    assert "AST 6.6" in subtitle
    assert "TS 0.7" in subtitle
