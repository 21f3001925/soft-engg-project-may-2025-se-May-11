#!/usr/bin/env bash

# Start Flask + Vue together; ctrl-c stops both
(
  cd backend
  poetry run flask --app app run --debug
) &
(
  cd frontend
  npm run dev
)