#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:5000}"
TIMESTAMP="$(date +%s)"
NAME="curl-test-${TIMESTAMP}"
EMAIL="curl-test-${TIMESTAMP}@example.com"
CONTENT="Testing timeline API with curl at ${TIMESTAMP}"

echo "Creating a timeline post..."
POST_RESPONSE="$(
  curl -sS -X POST "${BASE_URL}/api/timeline_post" \
    -d "name=${NAME}" \
    -d "email=${EMAIL}" \
    -d "content=${CONTENT}"
)"
echo "${POST_RESPONSE}"

POST_ID="$(
  POST_RESPONSE="${POST_RESPONSE}" python3 - <<'PY'
import json
import os

print(json.loads(os.environ["POST_RESPONSE"])["id"])
PY
)"

echo "Checking that the timeline post was added..."
GET_RESPONSE="$(curl -sS "${BASE_URL}/api/timeline_post")"
echo "${GET_RESPONSE}"

GET_RESPONSE="${GET_RESPONSE}" CONTENT="${CONTENT}" python3 - <<'PY'
import json
import os

response = json.loads(os.environ["GET_RESPONSE"])
content = os.environ["CONTENT"]
posts = response["timeline_posts"]

if not any(post["content"] == content for post in posts):
    raise SystemExit("Timeline post was not found in GET /api/timeline_post response")

print("Timeline post found in GET response.")
PY

echo "Deleting the test timeline post..."
curl -sS -X DELETE "${BASE_URL}/api/timeline_post/${POST_ID}"
echo
echo "curl-test.sh passed."
