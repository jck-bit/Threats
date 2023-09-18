#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate --no-input

gunicorn another_social_app.wsgi:application --bind 0.0.0.0:8000 &

unlink /etc/nginx/sites-enabled/default
nginx -g 'daemon off;'




