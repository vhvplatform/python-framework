#!/bin/sh
# Entrypoint script for flexible uvicorn configuration
# Note: uvloop and httptools are included in uvicorn[standard]

# Default values
WORKERS=${WORKERS:-4}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOOP=${LOOP:-uvloop}
HTTP=${HTTP:-httptools}
LOG_LEVEL=${LOG_LEVEL:-info}

# Run uvicorn with environment-based configuration
exec uvicorn framework.core.application:create_application \
    --host "$HOST" \
    --port "$PORT" \
    --factory \
    --workers "$WORKERS" \
    --loop "$LOOP" \
    --http "$HTTP" \
    --log-level "$LOG_LEVEL"
