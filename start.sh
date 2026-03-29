#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding database..."
python scripts/seed_data.py || echo "Database already seeded or seeding failed"

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
