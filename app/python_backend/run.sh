#!/usr/bin/env bash
# Start the FastAPI inference server (port 8000 by default)
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" -m uvicorn app.main:app --host 0.0.0.0 --port "${BACKEND_PORT:-8000}" --log-level info
