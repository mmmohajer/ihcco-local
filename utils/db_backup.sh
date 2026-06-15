#!/bin/bash

set -e
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

source "$ROOT_DIR/secrets/db/.env"

BACKUP_DIR="$ROOT_DIR/backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

docker exec chatbot-db-1 pg_dump \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    | gzip > "$BACKUP_FILE"

echo "Backup created:"
echo "$BACKUP_FILE"