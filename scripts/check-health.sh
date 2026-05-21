#!/usr/bin/env bash
set -euo pipefail

echo "Checking API health..."
curl -fsS http://localhost:8000/health | python3 -m json.tool
echo ""
echo "Checking web app reachability..."
curl -fsS -o /dev/null -w "Status: %{http_code}\n" http://localhost:3000
