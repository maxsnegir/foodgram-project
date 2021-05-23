#!/bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000