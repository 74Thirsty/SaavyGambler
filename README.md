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

## Disclaimer

Public sports APIs may enforce rate limits or require registration for an API
key. Ensure you comply with each provider's terms of service before using the
application in production.
