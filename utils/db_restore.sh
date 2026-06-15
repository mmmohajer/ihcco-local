#!/bin/bash

set -e
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

source "$ROOT_DIR/secrets/db/.env"

BACKUP_FILE="$ROOT_DIR/backups/db_20260611_113706.sql.gz"

echo "Dropping existing public schema..."

docker exec -i chatbot-db-1 psql \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "Restoring database..."

gunzip -c "$BACKUP_FILE" | docker exec -i chatbot-db-1 psql \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB"

echo "Database restored successfully."