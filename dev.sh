#!/usr/bin/env bash
# start Flask + Vue together; ctrl-c stops both
(
  cd backend
  source venv/bin/activate
  python app.py
) &
(
  cd frontend
  npm run dev
)
