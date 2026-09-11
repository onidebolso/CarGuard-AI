#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/carguard_api.log 2>&1 &
API_PID=$!
python -m http.server 8080 --directory frontend > /tmp/carguard_frontend.log 2>&1 &
FRONTEND_PID=$!

echo "API iniciada em http://localhost:8000"
echo "Frontend iniciado em http://localhost:8080"
echo "PIDs: API=$API_PID | FRONTEND=$FRONTEND_PID"

echo "Para encerrar: kill $API_PID $FRONTEND_PID"
