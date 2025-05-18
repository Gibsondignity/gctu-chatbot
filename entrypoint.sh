#!/bin/bash

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "PostgreSQL is up!"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
exec "$@"
