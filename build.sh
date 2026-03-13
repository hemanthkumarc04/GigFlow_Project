#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Collecting static files for production..."
python manage.py collectstatic --no-input

echo "Build process completed successfully!"
