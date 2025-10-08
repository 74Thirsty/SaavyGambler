"""Command line interface for StatTrackerPro."""
from __future__ import annotations

import argparse
import json
from datetime import date
from typing import List

import httpx

from .providers.thesportsdb import TheSportsDBProvider
from .services.analytics import AnalyticsService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="StatTrackerPro CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    league_parser = sub.add_parser("insights", help="Fetch event insights for a league")
    league_parser.add_argument("league_id", help="Identifier of the league")
    league_parser.add_argument(
        "--from-date",
        type=date.fromisoformat,
        help="Only include events on or after this ISO date",
    )

    fantasy_parser = sub.add_parser("fantasy", help="Generate fantasy projections")
    fantasy_parser.add_argument("player_ids", nargs="+", help="One or more player IDs")

    events_parser = sub.add_parser("events", help="Lookup events by identifier")
    events_parser.add_argument("event_ids", nargs="+", help="One or more event IDs")

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = AnalyticsService(TheSportsDBProvider())

    if args.command == "insights":
        try:
            insights = service.insights_for_league(args.league_id, from_date=args.from_date)
        except httpx.HTTPStatusError as exc:
            print(
                f"⚠️ No data found for league {args.league_id} ({exc.response.status_code})"
            )
            return 1
        print(json.dumps([_serialize_insight(insight) for insight in insights], default=str, indent=2))
        return 0

    if args.command == "fantasy":
        try:
            projections = service.fantasy_projections(args.player_ids)
        except httpx.HTTPStatusError as exc:
            print(
                "⚠️ No data found for the requested players "
                f"({exc.response.status_code})"
            )
            return 1
        print(json.dumps([projection.__dict__ for projection in projections], default=str, indent=2))
        return 0

    if args.command == "events":
        try:
            events = service.lookup_events(args.event_ids)
        except httpx.HTTPStatusError as exc:
            print(
                f"⚠️ No data found for the requested events ({exc.response.status_code})"
            )
            return 1
        print(json.dumps([_serialize_event(event) for event in events], default=str, indent=2))
        return 0

    parser.error("Unknown command")
    return 1


def _serialize_insight(insight):
    return {
        "event": insight.event.__dict__,
        "home_team": insight.home_team.__dict__,
        "away_team": insight.away_team.__dict__,
        "odds": insight.odds.__dict__ if insight.odds else None,
        "spread_prediction": insight.spread_prediction.__dict__,
        "total_prediction": insight.total_prediction.__dict__,
    }


def _serialize_event(event):
    return {
        "event_id": event.event_id,
        "date": event.event_date,
        "home_team": event.home_team_name or event.home_team_id,
        "away_team": event.away_team_name or event.away_team_id,
        "venue": event.venue,
        "status": event.status,
    }


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
