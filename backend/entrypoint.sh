#!/bin/sh

export DJANGO_SETTINGS_MODULE=backend.settings
# Initial sleep period (e.g., 5 seconds)
echo "Waiting for the database to start..."
sleep 5

# Check if the database is ready
echo "Checking if the database is up..."
for i in {1..30}; do
  if nc -z postgres 5432; then
    echo "Database is up!"
	echo "Running Database Migrations"
	python manage.py makemigrations
	python manage.py migrate

	exec "$@"
	daphne -b 0.0.0.0 -p 8080 backend.asgi:application
	exit 0
  fi
  echo "Waiting for the database... attempt $i"
  sleep 2
done

echo "Error: Could not connect to the database."
exit 1
