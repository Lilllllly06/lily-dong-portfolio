#!/bin/bash

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/root/lily-dong-portfolio}"
BRANCH="${BRANCH:-main}"
SERVICE_NAME="${SERVICE_NAME:-myportfolio}"

cd "$PROJECT_DIR"

git fetch origin
git reset "origin/${BRANCH}" --hard

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

systemctl restart "$SERVICE_NAME"
systemctl --no-pager status "$SERVICE_NAME"

echo "Redeployed $PROJECT_DIR from origin/$BRANCH and restarted $SERVICE_NAME"
