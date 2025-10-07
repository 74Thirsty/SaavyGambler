from stattrackerpro.models import PlayerStats
from stattrackerpro.services.fantasy import FantasyProjector, ScoringRule


def test_projector_orders_players_by_projection():
    projector = FantasyProjector(
        scoring_rules=[
            ScoringRule(metric="points_per_game", weight=1.0),
            ScoringRule(metric="assists_per_game", weight=2.0),
        ]
    )
    stats = [
        PlayerStats(player_id="1", name="A", points_per_game=10, assists_per_game=2),
        PlayerStats(player_id="2", name="B", points_per_game=15, assists_per_game=1),
    ]

    projections = projector.project(stats)

    assert projections[0].player_id == "2"
    assert projections[0].projected_points > projections[1].projected_points
