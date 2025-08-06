#!/usr/bin/env bash

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install Poetry to continue."
    echo "You can install Poetry by following the instructions at: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
poetry install
poetry run pre-commit install
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Installation complete!"
echo "To start the application, run: ./dev.sh"