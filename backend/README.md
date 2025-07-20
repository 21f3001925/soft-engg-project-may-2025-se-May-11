# Backend - Flask API

This is the backend service for the Senior Care web application, providing a RESTful API built with Flask. The backend handles all database operations, user authentication, and core business logic for medication management and appointment scheduling for senior citizens.

## Features

- User authentication and authorization
- Medication management system
- Caretaker monitoring features
- RESTful API endpoints
- Database integration
- Input validation and error handling

## Tech Stack

- **Framework:** [Flask](https://flask.palletsprojects.com/)
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Code Quality:**
  - [Black](https://black.readthedocs.io/) for code formatting
  - [Ruff](https://beta.ruff.rs/) for linting
  - [MyPy](https://mypy.readthedocs.io/) for type checking

## Prerequisites

- Python 3.13 or higher
- [Poetry](https://python-poetry.org/) for dependency management

## Project Setup

Install dependencies using Poetry:

```bash
poetry install
poetry run pre-commit install
```

## Development Server

Run the development server:

```bash
./dev.sh
```

The server will start at http://127.0.0.1:5000

## Linting and Formatting

- **Format Python files with Black:**
  ```bash
  black .
  ```
- **Lint Python files with Ruff:**
  ```bash
  ruff check .
  ```
- **Type check with MyPy:**
  ```bash
  mypy .
  ```

## Pre-commit Hooks

This project uses pre-commit hooks to automatically lint and format code before commits. If a commit fails, fix the reported issues and try again.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

---

For more information on Flask, check out the [Flask Documentation](https://flask.palletsprojects.com/).
