#!/bin/bash
cd ..

echo "Making migrations..."
python3 manage.py makemigrations

echo "Applying migrations..."
python3 manage.py migrate

echo "Starting server..."
python3 manage.py runserver