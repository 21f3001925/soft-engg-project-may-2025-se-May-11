#!/usr/bin/env bash

# Start Flask + Vue together; ctrl-c stops both
(
  cd backend
  poetry shell
  flask run
) &
(
  cd frontend
  npm run dev
)