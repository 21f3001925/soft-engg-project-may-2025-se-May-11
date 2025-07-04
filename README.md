# Senior Care App

This is the central repository for the Senior Care web application, a project for the Software Engineering course. The application is designed to help senior citizens manage their medication and appointment schedules, with a feature for caretakers to monitor their well-being.

## &#x1F680; Tech Stack

This project is built with a separated frontend and backend architecture:

- **Backend:** A RESTful API built with **[Flask](https://flask.palletsprojects.com/)**, a lightweight Python web framework.
- **Frontend:** A dynamic Single-Page Application (SPA) built with **[Vue.js](https://vuejs.org/)** and scaffolded using **[Vite](https://vitejs.dev/)** for a fast development experience.

## &#x1F4C1; Project Structure

The repository is organized into two main directories:

- `backend/`: Contains the Flask API server. All database logic, user authentication, and core business logic reside here. [**&#x2192; Go to Backend README**](./backend/README.md)
- `frontend/`: Contains the Vue.js client-side application. This is what users will see and interact with in their web browser. [**&#x2192; Go to Frontend README**](./frontend/README.md)

This separation allows the backend and frontend engineers to work independently.

## &#x1F527; Quick Start

To get the entire application up and running for development, follow these steps.

### Prerequisites

- **[Node.js](https://nodejs.org/)** (which includes `npm`). **Node.js version 16.0 or higher is required** for the frontend.
- **[Python](https://www.python.org/)**. **Python version 3.13.0 or higher is required** for the backend.
- **[Poetry](https://python-poetry.org/)** for the backend.

### 1. Installation

We have a convenient script to install all dependencies for both the frontend and backend. Run it from the root of the project:

```bash
./install.sh
```

This script will:

Navigate to the backend directory and run poetry install to create a virtual environment and install Python packages. Navigate to the frontend directory and run npm install to install all necessary JavaScript packages.

### 2. Running the Development Server

To start both the Flask backend API and the Vite frontend development server at the same time, run the following command from the project root:

```bash
./dev.sh
```

This script will:

Start the Flask API on http://127.0.0.1:5000.
Start the Vite + Vue dev server on http://127.0.0.1:5173 (or the next available port).
You can now open your browser to the frontend URL to see the application. To stop both servers, press Ctrl+C in your terminal.

## Pre-commit Hooks

This project uses pre-commit hooks to automatically lint and format code before commits. If a commit fails, fix the reported issues and try again.

---

For more information, check out the [Vue Docs](https://vuejs.org/guide/scaling-up/tooling.html#ide-support) and [Flask Documentation](https://flask.palletsprojects.com/).
