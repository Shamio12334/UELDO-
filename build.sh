#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install libraries
pip install -r requirements.txt

# Collect static files (CSS/Images)
python manage.py collectstatic --no-input

# Update database
python manage.py migrate