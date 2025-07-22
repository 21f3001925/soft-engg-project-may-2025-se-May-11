# Backend API Documentation

This document provides an overview of the RESTful APIs exposed by the backend service.

## Authentication API

Base URL: `/api/v1/auth`

### Purpose

This API is foundational for all user interactions, enabling secure user authentication and access to specific functionalities across the application. It ensures that only authorized users can access the system and its features.

### Signup

- **Endpoint:** `/api/v1/auth/signup`
- **Method:** `POST`
- **Description:** Registers a new user account (caregiver, senior citizen, or service provider).
- **Request Body Example:**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "senior_citizen"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Error Response Example (409 Conflict):**
  ```json
  {
    "msg": "Username or email already exists"
  }
  ```

### Login

- **Endpoint:** `/api/v1/auth/login`
- **Method:** `POST`
- **Description:** Authenticates a user with username and password, returning an access token.
- **Request Body Example:**
  ```json
  {
    "username": "testuser",
    "password": "password123"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Error Response Example (401 Unauthorized):**
  ```json
  {
    "msg": "Bad username or password"
  }
  ```

## OAuth API

Base URL: `/api/v1/oauth`

### Purpose

This API provides an alternative, convenient authentication method via Google, enhancing user accessibility and simplifying the login process for users who prefer to use existing accounts.

### Google Login

- **Endpoint:** `/api/v1/oauth/google/login`
- **Method:** `GET`
- **Description:** Initiates Google OAuth login flow. Redirects to Google's authentication page.
- **Response Example (302 Found):** Redirects to Google.

### Google Callback

- **Endpoint:** `/api/v1/oauth/google/callback`
- **Method:** `GET`
- **Description:** Callback URL for Google OAuth. Exchanges authorization code for tokens and logs in/registers the user.
- **Response Example (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Error Response Example (401 Unauthorized):**
  ```json
  {
    "msg": "Failed to get user info from Google."
  }
  ```

## Medications API

Base URL: `/api/v1/medications`

### Purpose

This API enables seniors to track their medication intake and allows caregivers to manage medication schedules. It ensures that seniors adhere to their medication regimens, which is essential for their health and safety.

### Get All Medications

- **Endpoint:** `/api/v1/medications`
- **Method:** `GET`
- **Description:** Retrieves all medications for the logged-in senior citizen, including details on dosage and whether taken.
- **Authentication:** JWT Required, Roles: `senior_citizen`, `caregiver`
- **Response Example (200 OK):**
  ```json
  [
    {
      "medication_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "name": "Aspirin",
      "dosage": "100mg",
      "time": "2025-07-18T08:00:00",
      "isTaken": false,
      "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
    }
  ]
  ```

### Add New Medication

- **Endpoint:** `/api/v1/medications`
- **Method:** `POST`
- **Description:** Adds a new medication for the logged-in senior citizen, including dosage and scheduled time.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Request Body Example:**
  ```json
  {
    "name": "Ibuprofen",
    "dosage": "200mg",
    "time": "2025-07-18T12:00:00",
    "isTaken": false
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "message": "Medication added",
    "medication_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```

### Get Medication by ID

- **Endpoint:** `/api/v1/medications/<string:medication_id>`
- **Method:** `GET`
- **Description:** Retrieves details for a specific medication by its unique ID.
- **Authentication:** JWT Required, Roles: `senior_citizen`, `caregiver`
- **Response Example (200 OK):**
  ```json
  {
    "medication_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Aspirin",
    "dosage": "100mg",
    "time": "2025-07-18T08:00:00",
    "isTaken": false,
    "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Medication not found"
  }
  ```

### Update Medication by ID

- **Endpoint:** `/api/v1/medications/<string:medication_id>`
- **Method:** `PUT`
- **Description:** Updates details for a specific medication by its ID, such as dosage or taken status.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Request Body Example:**
  ```json
  {
    "dosage": "250mg",
    "isTaken": true
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "medication_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Aspirin",
    "dosage": "250mg",
    "time": "2025-07-18T08:00:00",
    "isTaken": true,
    "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
  }
  ```

### Delete Medication by ID

- **Endpoint:** `/api/v1/medications/<string:medication_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific medication record by its ID.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Response Example (200 OK):**
  ```json
  {
    "message": "Medication deleted"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Medication not found"
  }
  ```

## Providers API

Base URL: `/api/v1/providers`

### Purpose

This API facilitates the management of service providers and their associated events. It allows service providers to create, update, and remove local events, and enables seniors to browse and join these social activities, promoting community engagement.

### Get All Service Providers

- **Endpoint:** `/api/v1/providers`
- **Method:** `GET`
- **Description:** Retrieves a list of all registered service providers.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (200 OK):**
  ```json
  [
    {
      "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "name": "Home Care Services",
      "contact_email": "contact@homecare.com",
      "phone_number": "123-456-7890",
      "services_offered": "Nursing, Cleaning"
    }
  ]
  ```

### Create New Service Provider

- **Endpoint:** `/api/v1/providers`
- **Method:** `POST`
- **Description:** Creates a new service provider entry in the system.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Request Body Example:**
  ```json
  {
    "name": "Elderly Support Inc.",
    "contact_email": "info@elderlysupport.com",
    "phone_number": "987-654-3210",
    "services_offered": "Companionship, Transportation"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Elderly Support Inc.",
    "contact_email": "info@elderlysupport.com",
    "phone_number": "987-654-3210",
    "services_offered": "Companionship, Transportation"
  }
  ```

### Get Service Provider by ID

- **Endpoint:** `/api/v1/providers/<string:provider_id>`
- **Method:** `GET`
- **Description:** Retrieves details for a specific service provider by their ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (200 OK):**
  ```json
  {
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Home Care Services",
    "contact_email": "contact@homecare.com",
    "phone_number": "123-456-7890",
    "services_offered": "Nursing, Cleaning"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Not Found"
  }
  ```

### Update Service Provider by ID

- **Endpoint:** `/api/v1/providers/<string:provider_id>`
- **Method:** `PUT`
- **Description:** Updates the information for a specific service provider by their ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Request Body Example:**
  ```json
  {
    "phone_number": "111-222-3333"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "Home Care Services",
    "contact_email": "contact@homecare.com",
    "phone_number": "111-222-3333",
    "services_offered": "Nursing, Cleaning"
  }
  ```

### Delete Service Provider by ID

- **Endpoint:** `/api/v1/providers/<string:provider_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific service provider record by their ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (204 No Content):** No content.
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Not Found"
  }
  ```

### Get Events for a Service Provider

- **Endpoint:** `/api/v1/providers/<string:provider_id>/events`
- **Method:** `GET`
- **Description:** Retrieves all events organized by a specific service provider.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (200 OK):**
  ```json
  [
    {
      "event_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
      "name": "Community Picnic",
      "date_time": "2025-08-01T14:00:00",
      "location": "Central Park",
      "description": "Annual community picnic for seniors.",
      "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    }
  ]
  ```

## Events API

Base URL: `/api/v1/events`

### Purpose

This API manages social events for senior citizens. It allows service providers to create, update, and delete event listings, while enabling seniors to browse and join activities. This feature is designed to promote social engagement and help seniors stay active and connected with their community.

### Get All Events

- **Endpoint:** `/api/v1/events`
- **Method:** `GET`
- **Description:** Retrieves a list of all available events.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (200 OK):**
  ```json
  [
    {
      "event_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
      "name": "Community Picnic",
      "date_time": "2025-08-01T14:00:00",
      "location": "Central Park",
      "description": "Annual community picnic for seniors.",
      "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    }
  ]
  ```

### Create New Event

- **Endpoint:** `/api/v1/events`
- **Method:** `POST`
- **Description:** Creates a new event entry.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Request Body Example:**
  ```json
  {
    "name": "Yoga Class",
    "date_time": "2025-07-25T10:00:00",
    "location": "Community Center",
    "description": "Weekly yoga class for all levels.",
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "event_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
    "name": "Yoga Class",
    "date_time": "2025-07-25T10:00:00",
    "location": "Community Center",
    "description": "Weekly yoga class for all levels.",
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```

### Get Event by ID

- **Endpoint:** `/api/v1/events/<string:event_id>`
- **Method:** `GET`
- **Description:** Retrieves details for a specific event by its ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (200 OK):**
  ```json
  {
    "event_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
    "name": "Community Picnic",
    "date_time": "2025-08-01T14:00:00",
    "location": "Central Park",
    "description": "Annual community picnic for seniors.",
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Not Found"
  }
  ```

### Update Event by ID

- **Endpoint:** `/api/v1/events/<string:event_id>`
- **Method:** `PUT`
- **Description:** Updates the information for a specific event by its ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Request Body Example:**
  ```json
  {
    "location": "Community Hall"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "event_id": "e1f2g3h4-i5j6-7890-1234-567890abcdef",
    "name": "Yoga Class",
    "date_time": "2025-07-25T10:00:00",
    "location": "Community Hall",
    "description": "Weekly yoga class for all levels.",
    "service_provider_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```

### Delete Event by ID

- **Endpoint:** `/api/v1/events/<string:event_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific event record by its ID.
- **Authentication:** JWT Required, Roles: `service_provider`
- **Response Example (204 No Content):** No content.
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Not Found"
  }
  ```

## Profile API

Base URL: `/api/v1/profile`

### Purpose

This API allows users to manage their profile information, including personal details, password changes, and avatar uploads. It also supports customization of user preferences, such as news categories, which is essential for a personalized user experience.

### Get User Profile

- **Endpoint:** `/api/v1/profile`
- **Method:** `GET`
- **Description:** Retrieves the profile information for the currently authenticated user.
- **Authentication:** JWT Required
- **Response Example (200 OK):**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "name": "Test User",
    "avatar_url": "/static/uploads/avatars/default.png"
  }
  ```

### Update User Profile

- **Endpoint:** `/api/v1/profile`
- **Method:** `PUT`
- **Description:** Updates the profile information for the currently authenticated user.
- **Authentication:** JWT Required
- **Request Body Example:**
  ```json
  {
    "name": "Updated Name"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "name": "Updated Name",
    "avatar_url": "/static/uploads/avatars/default.png"
  }
  ```

### Delete User Profile

- **Endpoint:** `/api/v1/profile`
- **Method:** `DELETE`
- **Description:** Deletes the profile for the currently authenticated user.
- **Authentication:** JWT Required
- **Response Example (204 No Content):** No content.

### Change User Password

- **Endpoint:** `/api/v1/profile/change-password`
- **Method:** `POST`
- **Description:** Allows the currently authenticated user to change their password.
- **Authentication:** JWT Required
- **Request Body Example:**
  ```json
  {
    "current_password": "oldpassword",
    "new_password": "newstrongpassword"
  }
  ```
- **Response Example (204 No Content):** No content.
- **Error Response Example (401 Unauthorized):**
  ```json
  {
    "message": "Invalid current password"
  }
  ```

### Upload User Avatar

- **Endpoint:** `/api/v1/profile/avatar`
- **Method:** `PUT`
- **Description:** Uploads a new avatar image for the currently authenticated user.
- **Authentication:** JWT Required
- **Request Body:** `multipart/form-data` with a `file` field.
- **Response Example (200 OK):**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "name": "Test User",
    "avatar_url": "/static/uploads/avatars/new_avatar.png"
  }
  ```
- **Error Response Example (400 Bad Request):**
  ```json
  {
    "message": "No file part"
  }
  ```

## News API

Base URL: `/api/v1/news`

### Purpose

This API provides seniors with access to news headlines from NewsAPI.org based on their selected topics of interest. This feature is designed to keep seniors informed and mentally engaged by delivering personalized content.

### Get News Categories

- **Endpoint:** `/api/v1/news/categories`
- **Method:** `GET`
- **Description:** Returns a list of available news categories that can be used for filtering news.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Response Example (200 OK):**
  ```json
  {
    "categories": [
      "business",
      "entertainment",
      "general",
      "health",
      "science",
      "sports",
      "technology"
    ]
  }
  ```

### Get Top Headlines

- **Endpoint:** `/api/v1/news/`
- **Method:** `GET`
- **Description:** Retrieves top news headlines from NewsAPI.org, with optional search query and category filters.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Query Parameters:**
  - `q` (optional): Search query.
  - `category` (optional): News category (e.g., `health`).
- **Response Example (200 OK):**
  ```json
  {
    "status": "ok",
    "totalResults": 10,
    "articles": [
      {
        "source": { "id": null, "name": "Example News" },
        "author": "John Doe",
        "title": "Example News Article",
        "description": "This is an example news article.",
        "url": "http://example.com/article",
        "urlToImage": "http://example.com/image.jpg",
        "publishedAt": "2025-07-18T10:00:00Z",
        "content": "..."
      }
    ]
  }
  ```
- **Error Response Example (502 Bad Gateway):**
  ```json
  {
    "message": "Failed to fetch news from NewsAPI."
  }
  ```

## Emergency Contacts API

Base URL: `/api/v1/emergency-contacts`

### Purpose

This API allows users to manage a senior's emergency contacts. It provides functionality to add, view, update, and delete contact information, ensuring that the right people can be notified promptly in a crisis.

### Get All Emergency Contacts

- **Endpoint:** `/api/v1/emergency-contacts`
- **Method:** `GET`
- **Description:** Retrieves all emergency contacts associated with the logged-in senior citizen.
- **Authentication:** JWT Required, Roles: `senior_citizen`, `caregiver`
- **Response Example (200 OK):**
  ```json
  [
    {
      "contact_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "name": "John Doe",
      "relation": "Son",
      "phone": "123-456-7890",
      "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
    }
  ]
  ```

### Add New Emergency Contact

- **Endpoint:** `/api/v1/emergency-contacts`
- **Method:** `POST`
- **Description:** Adds a new emergency contact for the logged-in senior citizen.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Request Body Example:**
  ```json
  {
    "name": "Jane Doe",
    "relation": "Daughter",
    "phone": "987-654-3210"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "message": "Emergency contact added",
    "contact_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```

### Get Emergency Contact by ID

- **Endpoint:** `/api/v1/emergency-contacts/<string:contact_id>`
- **Method:** `GET`
- **Description:** Retrieves details for a specific emergency contact by its ID.
- **Authentication:** JWT Required, Roles: `senior_citizen`, `caregiver`
- **Response Example (200 OK):**
  ```json
  {
    "contact_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "John Doe",
    "relation": "Son",
    "phone": "123-456-7890",
    "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Emergency contact not found"
  }
  ```

### Update Emergency Contact by ID

- **Endpoint:** `/api/v1/emergency-contacts/<string:contact_id>`
- **Method:** `PUT`
- **Description:** Updates the information for a specific emergency contact by its ID.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Request Body Example:**
  ```json
  {
    "phone": "111-222-3333"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "contact_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "name": "John Doe",
    "relation": "Son",
    "phone": "111-222-3333",
    "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
  }
  ```

### Delete Emergency Contact by ID

- **Endpoint:** `/api/v1/emergency-contacts/<string:contact_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific emergency contact record by its ID.
- **Authentication:** JWT Required, Roles: `caregiver`, `senior_citizen`
- **Response Example (200 OK):**
  ```json
  {
    "message": "Emergency contact deleted"
  }
  ```
- **Error Response Example (404 Not Found):**
  ```json
  {
    "message": "Emergency contact not found"
  }
  ```

## Emergency API

Base URL: `/api/v1/emergency`

### Purpose

This API handles the emergency alert system. When a senior citizen triggers an alert, this API is responsible for notifying their registered caregivers and emergency contacts. This provides a quick and effective way for seniors to request help, ensuring their safety and providing peace of mind for their loved ones.

### Trigger Emergency Alert

- **Endpoint:** `/api/v1/emergency/trigger`
- **Method:** `POST`
- **Description:** Triggers an emergency alert to registered caregivers and emergency contacts.
- **Authentication:** JWT Required
- **Response Example (200 OK):**
  ```json
  {
    "message": "Emergency alert triggered"
  }
  ```
- **Error Response Example (403 Forbidden):**
  ```json
  {
    "message": "Only senior citizens can trigger emergency alerts."
  }
  ```

## Reminder API

Base URL: `/api/v1/reminder`

### Purpose

This API is used to schedule and send reminders for appointments and other events. It allows users to set up multiple reminders, ensuring they receive timely notifications. This is a critical feature for helping seniors remember important events, which is essential for their health and well-being, and can be customized to meet individual needs.

### Schedule Reminder

- **Endpoint:** `/api/v1/reminder/schedule-reminder`
- **Method:** `POST`
- **Description:** Schedules reminders for appointments based on provided details.
- **Authentication:** JWT Required
- **Request Body Example:**
  ```json
  {
    "appointment_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "title": "Doctor's Visit",
    "location": "Clinic",
    "date_time": "2025-07-20T10:00:00",
    "email": "senior@example.com"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "message": "Reminders scheduled"
  }
  ```
- **Error Response Example (400 Bad Request):**
  ```json
  {
    "message": "Invalid date_time format"
  }
  ```

## Appointments API

Base URL: `/appointments`

### Purpose

This API is essential for managing appointments. It provides comprehensive endpoints for creating, viewing, updating, and deleting appointment details. This functionality is crucial for helping both seniors and their caregivers keep track of medical check-ups and other important dates, ensuring that no appointments are missed.

### Get All Appointments

- **Endpoint:** `/appointments`
- **Method:** `GET`
- **Description:** Retrieves all appointments for the logged-in senior citizen.
- **Response Example (200 OK):**
  ```json
  [
    {
      "appointment_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "title": "Doctor's Visit",
      "date_time": "2025-07-20T10:00:00",
      "location": "Clinic",
      "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
    }
  ]
  ```

### Create Appointment

- **Endpoint:** `/appointments`
- **Method:** `POST`
- **Description:** Creates a new appointment for the logged-in senior citizen.
- **Request Body Example:**
  ```json
  {
    "title": "Dentist Appointment",
    "date_time": "2025-07-22T14:30:00",
    "location": "Dental Office",
    "senior_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210"
  }
  ```
- **Response Example (201 Created):**
  ```json
  {
    "message": "Appointment created",
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
  }
  ```

### Update Appointment

- **Endpoint:** `/appointments/<uuid:appointment_id>`
- **Method:** `PUT`
- **Description:** Updates a specific appointment by its ID.
- **Request Body Example:**
  ```json
  {
    "location": "New Clinic Address"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "message": "Appointment updated"
  }
  ```

### Delete Appointment

- **Endpoint:** `/appointments/<uuid:appointment_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific appointment by its ID.
- **Response Example (200 OK):**
  ```json
  {
    "message": "Appointment deleted"
  }
  ```
