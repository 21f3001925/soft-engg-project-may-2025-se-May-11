# Frontend - Vue 3 + Vite

This is the frontend application for the Senior Care web application, built with Vue 3 and Vite. The frontend provides a modern, responsive user interface for senior citizens to manage their medications and appointments, and for caretakers to monitor their well-being.

## Features

- **Multi-Role Dashboards**: Tailored interfaces for senior citizens, caregivers, and service providers
- **Medication Management**: Schedule, track, and manage medications with visual progress indicators
- **Appointment System**: Create, edit, and manage appointments
- **Emergency Contacts**: Quick access to emergency contacts with one-tap calling functionality
- **Social Hub**: Discover and join local community events with real-time updates
- **News Feed**: Personalized news content with search and filtering capabilities
- **Accessibility**: Dark mode, adjustable font sizes, and responsive design for better usability
- **User Authentication**: Secure login with email/phone and Google OAuth integration

## Tech Stack

- **Framework:** [Vue 3](https://vuejs.org/) with Composition API
- **Build Tool:** [Vite](https://vitejs.dev/) for fast development and building
- **State Management:** [Pinia](https://pinia.vuejs.org/) for reactive state management
- **Routing:** [Vue Router](https://router.vuejs.org/) for SPA navigation
- **UI Components:** Custom components with [Tailwind CSS](https://tailwindcss.com/) for styling
- **Icons:** [Lucide Vue](https://lucide.dev/guide/packages/lucide-vue-next) for consistent iconography
- **Code Quality:**
  - [ESLint](https://eslint.org/) for linting with Vue-specific rules
  - [Prettier](https://prettier.io/) for code formatting

## Prerequisites

- Node.js 16.x or higher
- npm 7.x or higher

## Project Setup

Install dependencies:

```bash
npm install
```

## Development Server

Start the development server:

```bash
npm run dev
```

The application will be available at http://127.0.0.1:5173 (or the next available port)

## Build for Production

Create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

## Linting and Formatting

- **Lint JS/Vue files:**
  ```bash
  npx eslint .
  ```
- **Fix lint errors automatically:**
  ```bash
  npx eslint . --fix
  ```
- **Format files with Prettier:**
  ```bash
  npx prettier --write .
  ```

## Pre-commit Hooks

This project uses pre-commit hooks to automatically lint and format code before commits. If a commit fails, fix the reported issues and try again.

## Accessibility

The application includes several accessibility features:

- **Dark Mode**: Toggle between light and dark themes
- **Font Size Adjustment**: Small, medium, and large text options

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

---

For more information on Vue 3 and Vite, check out the [Vue Docs](https://vuejs.org/guide/scaling-up/tooling.html#ide-support) and [Vite Docs](https://vitejs.dev/).
