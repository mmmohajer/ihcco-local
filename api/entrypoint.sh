#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! python -c "
import os
import psycopg2

psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    dbname=os.getenv('DB_NAME')
)
"; do
    echo "PostgreSQL unavailable - sleeping"
    sleep 2
done

echo "Running migrations..."

alembic upgrade head

echo "Starting API..."

exec "$@"