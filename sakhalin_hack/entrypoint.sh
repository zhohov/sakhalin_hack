#!/bin/sh

python src/manage.py makemigrations
python src/manage.py migrate --no-input
python src/manage.py collectstatic --no-input

cd src/
gunicorn core.wsgi:application --bind 0.0.0.0:8000
