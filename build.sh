#!/bin/bash

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migrations..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear