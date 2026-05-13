# home-backend

Python FastAPI backend for the Home project.

## Development

```bash
uv sync
cp .env.example .env
uv run uvicorn home.app:app --host 0.0.0.0 --port 45600 --reload
```

The service uses SQLite by default and creates seed site links on startup.
