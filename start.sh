#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 2

echo "Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migrations failed!"
    exit 1
fi

echo "Seeding database..."
python scripts/seed_data.py || echo "⚠️  Database already seeded or seeding failed (non-critical)"

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
