# Backend - Flask API

This is the backend service for the Senior Care web application, providing a RESTful API built with Flask. The backend handles all database operations, user authentication, and core business logic for medication management and appointment scheduling for senior citizens.

## Features

- User authentication and authorization
- Medication management system
- AI-powered document analysis using Google Gemini API, with text extraction from PDFs and images (OCR).
- Caretaker monitoring features
- RESTful API endpoints
- Database integration
- Input validation and error handling

## Tech Stack

- **Framework:** [Flask](https://flask.palletsprojects.com/) with Flask-RESTful
- **Database:** [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) ORM with SQLite
- **Authentication:** [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) for JWT tokens
- **API Documentation:** [Flask-Smorest](https://flask-smorest.readthedocs.io/) for OpenAPI/Swagger docs
- **AI & Document Processing:**
  - [Google Gemini API](https://ai.google.dev/) for summarization and Q&A
  - [PyPDF2](https://pypdf2.readthedocs.io/) & [Pytesseract](https://github.com/madmaze/pytesseract) for text and OCR extraction
  - [pdf2image](https://github.com/Belval/pdf2image) & [Pillow](https://python-pillow.org/) for PDF-to-image conversion
  - [fpdf2](https://github.com/py-pdf/fpdf2) for PDF generation
- **OAuth:** [Authlib](https://authlib.org/) with Google OAuth for social login
- **News API:** [NewsAPI](https://newsapi.org/) for news content
- **Task Queue:** [Celery](https://docs.celeryproject.org/) with Redis for background tasks
- **Scheduling:** [APScheduler](https://apscheduler.readthedocs.io/) for task scheduling
- **Email:** [Flask-Mail](https://pythonhosted.org/Flask-Mail/) for email notifications
- **SMS:** [Twilio](https://www.twilio.com/) for SMS notifications
- **Code Quality:**
  - [Black](https://black.readthedocs.io/) for code formatting
  - [Ruff](https://beta.ruff.rs/) for linting
  - [MyPy](https://mypy.readthedocs.io/) for type checking

## Prerequisites

- Python 3.13 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- **[Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract#installing-tesseract)**: Required for the AI report analysis feature. Please follow the installation instructions for your operating system.

## Project Setup

Install dependencies using Poetry:

```bash
poetry install
```

## Development Server

Run the development server:

```bash
./dev.sh
```

The server will start at http://127.0.0.1:5001

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

## Testing

### Running Tests

Run the complete test suite:

```bash
poetry run pytest
```

Run tests with verbose output:

```bash
poetry run pytest -v
```

### Running Specific Tests

Run specific test files:

```bash
poetry run pytest tests/test_emergency_contacts.py
poetry run pytest tests/test_news.py
poetry run pytest tests/test_oauth.py
poetry run pytest tests/test_providers.py
```

Run a single test function:

```bash
poetry run pytest tests/test_auth.py::test_login_success
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

---

For more information on Flask, check out the [Flask Documentation](https://flask.palletsprojects.com/).
