![Sheen Banner](https://raw.githubusercontent.com/74Thirsty/74Thirsty/main/assets/statpro.svg)


# SaavyGambler

SaavyGambler is a production-grade toolkit that helps fantasy sports players
and bettors track statistics, fetch real-time data from public APIs, and
calculate predictive insights such as point spreads, totals, and win
probabilities.

## Features

- **Provider Abstraction** – Robust HTTP client with caching, retry logic, and
  an implementation for the [TheSportsDB](https://www.thesportsdb.com/) public
  API.
- **Free Event Lookups** – Quickly fetch specific fixtures from TheSportsDB's
  free tier by supplying event identifiers.
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
   and cache locations. When no key is supplied SaavyGambler automatically
   uses TheSportsDB's free lookup tier, so you can get started without signing
   up for an account:

   ```env
   gambler_sportsdb_api_key=YOUR_API_KEY
   gambler_cache_dir=.cache
   ```

3. Run the FastAPI service:

   ```bash
   uvicorn gambler.app.main:app --reload
   ```

4. Use the CLI:

   ```bash
   gambler insights 4328
   gambler fantasy 34145937
   gambler events 2052711 2052712 2052713 2052714
   ```

   The ``events`` command looks up fixtures by ID using the free
   [TheSportsDB lookup endpoint](https://www.thesportsdb.com/api.php). No
   payment or subscription is required—just pass the identifiers you care
   about and the CLI will return the scheduled date along with the home and
   away teams.

## Graphical Interface

Install the optional GUI dependencies and launch the modern KivyMD-powered
interface:

```bash
pip install -e .[gui]
gambler-gui
```

The desktop application exposes three tabs:

- **Teams** – search TheSportsDB for teams by name and view records and scoring
  trends.
- **Events** – look up specific fixtures by their identifier to see the matchup,
  date, venue, and status.
- **Players** – retrieve player box score averages and any custom metrics
  exposed by the data provider.

## Building an Android APK

Use [Buildozer](https://github.com/kivy/buildozer) to generate an APK from the
same KivyMD interface:

```bash
pip install buildozer
cd android
buildozer -v android debug
```

The provided ``android/buildozer.spec`` file points Buildozer at the
``gui_main.py`` helper script in the project root, which bootstraps the GUI. The
resulting APK can be found in ``android/bin`` after a successful build.

### Play Store release builds

To ship the exact same interface to the Play Store, populate the release
signing fields in ``android/buildozer.spec``. You can edit the file directly or
fill the blank entries from environment variables:

```bash
export ANDROID_KEYSTORE_PATH=/absolute/path/to/saavygambler.keystore
export ANDROID_KEYSTORE_PASSWORD=your_keystore_password
export ANDROID_KEYALIAS=saavygambler
export ANDROID_KEYALIAS_PASSWORD=your_alias_password

python - <<'PY'
import configparser, os, pathlib
spec_path = pathlib.Path('android/buildozer.spec')
config = configparser.ConfigParser()
config.read(spec_path)
section = config['app']
section['android.release_keystore'] = os.environ['ANDROID_KEYSTORE_PATH']
section['android.release_keyalias'] = os.environ['ANDROID_KEYALIAS']
section['android.keystore_password'] = os.environ['ANDROID_KEYSTORE_PASSWORD']
section['android.keyalias_password'] = os.environ['ANDROID_KEYALIAS_PASSWORD']
with spec_path.open('w') as fh:
    config.write(fh)
PY
```

Then build the signed release artifact:

```bash
cd android
buildozer -v android release
```

Buildozer produces a zip-aligned, Play Store ready ``*-release.apk`` inside
``android/bin`` using the same KivyMD code path as the debug build. After the
build completes you can restore the original spec with ``git checkout --
android/buildozer.spec`` and verify the signature using ``apksigner verify
--print-certs`` before uploading to the Play Console.

## Testing

Run the automated test suite with:

```bash
pytest
```

From those package metadata files, here’s what the **SaavyGambler** FastAPI service actually does:

---

### 🧠 **High-level purpose**

`SaavyGambler` is a **sports statistics and analytics service** built around FastAPI.
It exposes API endpoints (via `saavygambler/app/main.py`) for **collecting**, **analyzing**, and **predicting** sports data — likely for fantasy sports or performance tracking.

---

### ⚙️ **Architecture from SOURCES.txt**

The module layout tells us how the service works:

| Path                                      |  Role                                                                              |
| ----------------------------------------- |  --------------------------------------------------------------------------------  |
| `saavygambler/app/main.py`                | The FastAPI entry point — defines routes, starts the HTTP server.                  |
| `saavygambler/app/schemas.py`             | Pydantic schemas for request/response validation.                                  |
| `saavygambler/providers/api_client.py`    | Asynchronous HTTP client (probably wraps external APIs like TheSportsDB).          |
| `saavygambler/providers/thesportsdb.py`   | Integration with the [TheSportsDB](https://www.thesportsdb.com/) sports stats API. |
| `saavygambler/services/stat_collector.py` | Core data ingestion service; pulls stats from providers into structured models.    |
| `saavygambler/services/analytics.py`      | Performs derived analytics — aggregates player or team metrics.                    |
| `saavygambler/services/fantasy.py`        | Fantasy scoring and roster projection logic.                                       |
| `saavygambler/services/prediction.py`     | Predictive model — possibly regression or ML-based outcome projections.            |
| `saavygambler/models.py`                  | ORM or domain models for teams, players, games, etc.                               |
| `saavygambler/config.py`                  | Environment/configuration loading.                                                 |
| `saavygambler/cli.py`                     | Command-line interface to run or manage the app.                                   |

---

### 🚀 **How it runs**

The command you gave:

```bash
uvicorn gambler.app.main:app --reload
```

starts the **FastAPI** app defined in `main.py`.
That file (typical pattern) looks like:

```python
from fastapi import FastAPI
from gambler.services import stat_collector, analytics, prediction, fantasy

app = FastAPI(title="SaavyGambler")

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

The **FastAPI service** in SaavyGambler is an API gateway that:

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
