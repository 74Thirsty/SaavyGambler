"""Fantasy projection utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from ..models import FantasyProjection, PlayerStats


@dataclass
class ScoringRule:
    metric: str
    weight: float


DEFAULT_RULES = [
    ScoringRule(metric="points_per_game", weight=1.0),
    ScoringRule(metric="rebounds_per_game", weight=1.2),
    ScoringRule(metric="assists_per_game", weight=1.5),
]


class FantasyProjector:
    """Generate fantasy projections from player statistics."""

    def __init__(self, scoring_rules: Optional[Iterable[ScoringRule]] = None) -> None:
        self.scoring_rules = list(scoring_rules) if scoring_rules else list(DEFAULT_RULES)

    def project(self, stats: List[PlayerStats]) -> List[FantasyProjection]:
        projections: List[FantasyProjection] = []
        for player in stats:
            projected_points = 0.0
            metadata: Dict[str, float] = {}
            for rule in self.scoring_rules:
                value = getattr(player, rule.metric, None) or player.custom_metrics.get(rule.metric)
                if value is None:
                    continue
                contribution = value * rule.weight
                metadata[rule.metric] = contribution
                projected_points += contribution
            floor = projected_points * 0.85
            ceiling = projected_points * 1.15
            projections.append(
                FantasyProjection(
                    player_id=player.player_id,
                    name=player.name,
                    projected_points=projected_points,
                    floor=floor,
                    ceiling=ceiling,
                    metadata=metadata,
                )
            )
        projections.sort(key=lambda p: p.projected_points, reverse=True)
        return projections


__all__ = ["FantasyProjector", "ScoringRule", "DEFAULT_RULES"]
