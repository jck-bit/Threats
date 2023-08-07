#!/bin/bash

echo "Building the project..."
python3.9 -m pip install -r requirements.txt


# activate virtual environment
# python3.9 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

python3.9 manage.py collectstatic 