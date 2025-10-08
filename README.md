![Sheen Banner](https://raw.githubusercontent.com/74Thirsty/74Thirsty/main/assets/statpro.svg)


# StatTrackerPro

StatTrackerPro is a production-grade toolkit that helps fantasy sports players
and bettors track statistics, fetch real-time data from public APIs, and
calculate predictive insights such as point spreads, totals, and win
probabilities.

## Features

- **Provider Abstraction** – Robust HTTP client with caching, retry logic, and
  an implementation for the [TheSportsDB](https://www.thesportsdb.com/) public
  API.
- **Prediction Engine** – Algorithms to estimate spreads, totals, and moneyline
  edges using team performance metrics.
- **Fantasy Projections** – Flexible scoring rules to produce player fantasy
  point projections with floor/ceiling ranges.
- **FastAPI Service** – REST API exposing health checks, league insights, and
  fantasy projection endpoints.
- **CLI Utility** – Command line interface for fetching insights or generating
  projections.

## Getting Started

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[server]
   ```

2. (Optional) set environment variables in a `.env` file to configure API keys
   and cache locations:

   ```env
   stattrackerpro_sportsdb_api_key=YOUR_API_KEY
   stattrackerpro_cache_dir=.cache
   ```

3. Run the FastAPI service:

   ```bash
   uvicorn stattrackerpro.app.main:app --reload
   ```

4. Use the CLI:

   ```bash
   stattrackerpro insights 4328
   stattrackerpro fantasy 34145937
   ```

## Testing

Run the automated test suite with:

```bash
pytest
```

From those package metadata files, here’s what the **StatTrackerPro** FastAPI service actually does:

---

### 🧠 **High-level purpose**

`stattrackerpro` is a **sports statistics and analytics service** built around FastAPI.
It exposes API endpoints (via `stattrackerpro/app/main.py`) for **collecting**, **analyzing**, and **predicting** sports data — likely for fantasy sports or performance tracking.

---

### ⚙️ **Architecture from SOURCES.txt**

The module layout tells us how the service works:

| Path                                        | Role                                                                               |
| ------------------------------------------- | ---------------------------------------------------------------------------------- |
| `stattrackerpro/app/main.py`                | The FastAPI entry point — defines routes, starts the HTTP server.                  |
| `stattrackerpro/app/schemas.py`             | Pydantic schemas for request/response validation.                                  |
| `stattrackerpro/providers/api_client.py`    | Asynchronous HTTP client (probably wraps external APIs like TheSportsDB).          |
| `stattrackerpro/providers/thesportsdb.py`   | Integration with the [TheSportsDB](https://www.thesportsdb.com/) sports stats API. |
| `stattrackerpro/services/stat_collector.py` | Core data ingestion service; pulls stats from providers into structured models.    |
| `stattrackerpro/services/analytics.py`      | Performs derived analytics — aggregates player or team metrics.                    |
| `stattrackerpro/services/fantasy.py`        | Fantasy scoring and roster projection logic.                                       |
| `stattrackerpro/services/prediction.py`     | Predictive model — possibly regression or ML-based outcome projections.            |
| `stattrackerpro/models.py`                  | ORM or domain models for teams, players, games, etc.                               |
| `stattrackerpro/config.py`                  | Environment/configuration loading.                                                 |
| `stattrackerpro/cli.py`                     | Command-line interface to run or manage the app.                                   |

---

### 🚀 **How it runs**

The command you gave:

```bash
uvicorn stattrackerpro.app.main:app --reload
```

starts the **FastAPI** app defined in `main.py`.
That file (typical pattern) looks like:

```python
from fastapi import FastAPI
from stattrackerpro.services import stat_collector, analytics, prediction, fantasy

app = FastAPI(title="StatTrackerPro")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/stats/{team}")
async def team_stats(team: str):
    return await stat_collector.get_team_stats(team)

@app.get("/fantasy/project/{player}")
async def fantasy_projection(player: str):
    return await fantasy.project_player(player)

@app.get("/predict/game/{id}")
async def predict_game(id: str):
    return await prediction.predict_game(id)
```

So it acts as a **REST API** that wraps service modules under clean HTTP endpoints.

When you run it:

* FastAPI spins up under Uvicorn.
* The app imports `stat_collector`, which fetches data from TheSportsDB.
* Analytics, fantasy, and prediction modules operate on that data to provide real-time metrics and forecasts.

---

### 📊 **Typical API surface**

Based on its services, you can expect endpoints like:

```
GET /teams/{team_id}/stats          → returns team statistics
GET /players/{player_id}/fantasy    → fantasy score projections
GET /games/{game_id}/predict        → predicted outcomes or win probabilities
GET /analytics/leaderboard          → computed leaderboards or efficiency metrics
```

All responses are likely Pydantic-validated (`schemas.py`) JSON payloads.

---

### 💡 **In short**

The **FastAPI service** in StatTrackerPro is an API gateway that:

* Connects to third-party sports data sources (TheSportsDB, etc.),
* Ingests live or cached game/player/team data,
* Runs analytics and prediction routines,
* Serves that information via REST endpoints for use in fantasy or stat-tracking applications.

So:
**It’s a complete sports analytics microservice.**
FastAPI is just the web layer; the actual brain sits in those `services/*` modules.


## Disclaimer

Public sports APIs may enforce rate limits or require registration for an API
key. Ensure you comply with each provider's terms of service before using the
application in production.
