import sys
import types
from datetime import date


httpx_stub = types.ModuleType("httpx")


class _DummyHTTPError(Exception):
    pass


class _DummyRequestError(Exception):
    pass


class _DummyClient:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):  # pragma: no cover - defensive stub
        raise NotImplementedError("HTTP client not available in tests")

    def close(self) -> None:
        pass


httpx_stub.Client = _DummyClient
httpx_stub.HTTPStatusError = _DummyHTTPError
httpx_stub.RequestError = _DummyRequestError
sys.modules.setdefault("httpx", httpx_stub)

from stattrackerpro.models import Event
from stattrackerpro.providers.thesportsdb import TheSportsDBProvider


class DummyClient:
    def __init__(self, *, league_payload=None, event_payloads=None):
        self.league_payload = league_payload or {}
        self.event_payloads = event_payloads or {}
        self.requests = []

    def get_json(self, url, *, params=None, **kwargs):  # pragma: no cover - exercised in tests
        self.requests.append({"url": url, "params": params})
        if url.endswith("eventsnextleague.php"):
            return self.league_payload
        if url.endswith("lookupevent.php"):
            event_id = params.get("id") if params else None
            return self.event_payloads.get(event_id, {"events": []})
        raise AssertionError(f"Unexpected URL: {url}")


def test_lookup_events_returns_named_events():
    payloads = {
        "2052711": {
            "events": [
                {
                    "idEvent": "2052711",
                    "idLeague": "1234",
                    "idHomeTeam": "5678",
                    "idAwayTeam": "91011",
                    "dateEvent": "2024-01-10",
                    "strVenue": "Awesome Arena",
                    "strStatus": "Scheduled",
                    "intHomeScore": None,
                    "intAwayScore": None,
                    "strHomeTeam": "Home Heroes",
                    "strAwayTeam": "Road Warriors",
                }
            ]
        }
    }
    provider = TheSportsDBProvider(client=DummyClient(event_payloads=payloads))

    events = provider.lookup_events(["2052711"])

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, Event)
    assert event.event_id == "2052711"
    assert event.home_team_name == "Home Heroes"
    assert event.away_team_name == "Road Warriors"
    assert event.event_date == date(2024, 1, 10)


def test_get_events_includes_team_names():
    league_payload = {
        "events": [
            {
                "idEvent": "8888",
                "idLeague": "555",
                "idHomeTeam": "100",
                "idAwayTeam": "200",
                "dateEvent": "2024-02-01",
                "strHomeTeam": "Alpha",
                "strAwayTeam": "Beta",
            }
        ]
    }
    provider = TheSportsDBProvider(client=DummyClient(league_payload=league_payload))

    events = provider.get_events("555")

    assert len(events) == 1
    event = events[0]
    assert event.home_team_name == "Alpha"
    assert event.away_team_name == "Beta"
    assert event.event_date == date(2024, 2, 1)
