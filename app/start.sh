#!/usr/bin/env bash
# Production entry point: FastAPI inference server (background) + Express server (foreground).
set -e
cd "$(dirname "$0")"
(cd python_backend && ./run.sh) &
exec node dist/index.cjs
