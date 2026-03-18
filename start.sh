#!/usr/bin/env bash
# start.sh - Render Start Command

echo "Running migrations before starting server..."
python manage.py migrate --no-input

echo "Starting Daphne server..."
daphne -b 0.0.0.0 -p ${PORT:-8000} config.asgi:application