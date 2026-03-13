#!/usr/bin/env bash
# exit on error
set -o errexit

if [ -z "$DATABASE_URL" ]; then
    echo "WARNING: DATABASE_URL is not set. Falling back to SQLite."
else
    echo "DATABASE_URL is set (PostgreSQL connection available)."
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Collecting static files for production..."
python manage.py collectstatic --no-input

echo "Build process completed successfully!"
