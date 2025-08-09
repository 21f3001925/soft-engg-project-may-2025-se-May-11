#!/usr/bin/env bash

(
  cd backend
  poetry run gunicorn --bind 127.0.0.1:5000 --reload "app:app"
) &
BACKEND_PID=$!

( cd frontend; npm run dev ) &
FRONTEND_PID=$!

cleanup() {
    echo "Shutting down servers..."

    if [ -n "$BACKEND_PID" ]; then
        kill -TERM $BACKEND_PID 2>/dev/null
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill -TERM $FRONTEND_PID 2>/dev/null
    fi

    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null

    echo "Forcing shutdown of any remaining processes..."

    lsof -ti:5000 | xargs kill -9 2>/dev/null
    pkill -f "node.*npm" 2>/dev/null
    pkill -f "gunicorn" 2>/dev/null

    echo "Servers shut down."
}

trap cleanup SIGINT

wait $BACKEND_PID
wait $FRONTEND_PID