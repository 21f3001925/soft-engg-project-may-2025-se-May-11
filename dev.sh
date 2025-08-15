#!/usr/bin/env bash

(
  cd backend
  poetry run gunicorn --bind 127.0.0.1:5001 --reload "app:app"
) &
BACKEND_PID=$!

( cd frontend; npm run dev ) &
FRONTEND_PID=$!

# Start Celery worker
(
  cd backend
  poetry run celery -A celery_app worker --loglevel=info
) &
CELERY_WORKER_PID=$!

# Start Celery beat scheduler
(
  cd backend
  poetry run celery -A celery_app beat --loglevel=info
) &
CELERY_BEAT_PID=$!

cleanup() {
    echo "Shutting down servers..."

    if [ -n "$BACKEND_PID" ]; then
        kill -TERM $BACKEND_PID 2>/dev/null
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill -TERM $FRONTEND_PID 2>/dev/null
    fi
    if [ -n "$CELERY_WORKER_PID" ]; then
        kill -TERM $CELERY_WORKER_PID 2>/dev/null
    fi
    if [ -n "$CELERY_BEAT_PID" ]; then
        kill -TERM $CELERY_BEAT_PID 2>/dev/null
    fi

    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null
    wait $CELERY_WORKER_PID 2>/dev/null
    wait $CELERY_BEAT_PID 2>/dev/null

    echo "Forcing shutdown of any remaining processes..."

    lsof -ti:5001 | xargs kill -9 2>/dev/null
    pkill -f "node.*npm" 2>/dev/null
    pkill -f "gunicorn" 2>/dev/null
    pkill -f "celery" 2>/dev/null

    echo "Servers shut down."
}

trap cleanup SIGINT

wait $BACKEND_PID
wait $FRONTEND_PID
wait $CELERY_WORKER_PID
wait $CELERY_BEAT_PID