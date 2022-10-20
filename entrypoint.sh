#!/bin/bash
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
python manage.py create-superuser --username "$DJANGO_ADMIN_NAME" --password "$DJANGO_ADMIN_PASSWORD" --email "$DJANGO_ADMIN_EMAIL"
exec gunicorn vcs_site.wsgi:application --bind 0.0.0.0:8000
