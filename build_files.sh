#!/bin/bash

echo "Building event booking project..."
python -m pip install -r requirements.txt

echo "Migrate database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed."