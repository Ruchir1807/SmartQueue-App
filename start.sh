#!/bin/bash
set -o errexit  

# Activate virtual environment (optional if Railpack auto-installs deps)
. venv/bin/activate || true

# Run migrations
python smartqueue/smartqueue/manage.py migrate --noinput

# Collect static files
python smartqueue/smartqueue/manage.py collectstatic --noinput

# Start Gunicorn
gunicorn smartqueue.smartqueue.smartqueue.wsgi:application --bind 0.0.0.0:$PORT

