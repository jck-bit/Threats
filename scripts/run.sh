#!/bin/sh

set -e

python manage.py wait__for__db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module another_social_app.wsgi
