#!/bin/bash

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/root/lily-dong-portfolio}"

cd "$PROJECT_DIR"

git fetch
git reset origin/main --hard

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

echo "Redeployed $PROJECT_DIR from origin/main using Docker Compose"
