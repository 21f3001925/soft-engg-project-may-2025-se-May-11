# Backend API Documentation

This document provides an overview of the RESTful APIs exposed by the backend service.

## Authentication API

Base URL: `/api/v1/auth`

### Supported User Stories

This API is foundational for all user stories requiring user authentication (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13). It enables users to log in and access their specific functionalities.

### Signup

- **Endpoint:** `/api/v1/auth/signup`
- **Method:** `POST`
- **Description:** Creates a new user account.
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
- **Description:** Logs in a user and returns an access token.
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

### Supported User Stories

This API supports user stories (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13) by providing an alternative, convenient authentication method via Google, enhancing user accessibility and simplifying the login process.

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

### Supported User Stories

This API directly supports User Story 1 (senior marking medication as taken) and User Story 9 (caregiver managing medications).

### Get All Medications

- **Endpoint:** `/api/v1/medications`
- **Method:** `GET`
- **Description:** Retrieves all medications for the logged-in senior citizen.
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
- **Description:** Adds a new medication for the logged-in senior citizen.
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
- **Description:** Retrieves a specific medication by its ID.
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
- **Description:** Updates a specific medication by its ID.
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
- **Description:** Deletes a specific medication by its ID.
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

### Supported User Stories

This API supports User Story 6 (senior browsing and joining local social events) and User Story 13 (service provider creating/updating/removing local events).

### Get All Service Providers

- **Endpoint:** `/api/v1/providers`
- **Method:** `GET`
- **Description:** Retrieves all service providers.
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
- **Description:** Creates a new service provider.
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
- **Description:** Retrieves a specific service provider by its ID.
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
- **Description:** Updates a specific service provider by its ID.
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
- **Description:** Deletes a specific service provider by its ID.
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
- **Description:** Retrieves all events associated with a specific service provider.
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

### Supported User Stories

This API directly supports User Story 6 (senior browsing and joining local social events) and User Story 13 (service provider creating/updating/removing local events).

### Get All Events

- **Endpoint:** `/api/v1/events`
- **Method:** `GET`
- **Description:** Retrieves all events.
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
- **Description:** Creates a new event.
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
- **Description:** Retrieves a specific event by its ID.
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
- **Description:** Updates a specific event by its ID.
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
- **Description:** Deletes a specific event by its ID.
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

### Supported User Stories

This API supports user stories by allowing users to manage their profile information, which is essential for personalized experiences across all functionalities (e.g., User Story 7 for accessibility settings, and implicitly for all stories requiring user identification).

### Get User Profile

- **Endpoint:** `/api/v1/profile`
- **Method:** `GET`
- **Description:** Retrieves the logged-in user's profile information.
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
- **Description:** Updates the logged-in user's profile information.
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
- **Description:** Deletes the logged-in user's profile.
- **Authentication:** JWT Required
- **Response Example (204 No Content):** No content.

### Change User Password

- **Endpoint:** `/api/v1/profile/change-password`
- **Method:** `POST`
- **Description:** Changes the logged-in user's password.
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
- **Description:** Uploads a new avatar for the logged-in user.
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

### Supported User Stories

This API directly supports User Story 3 (senior receiving daily news updates).

### Get News Categories

- **Endpoint:** `/api/v1/news/categories`
- **Method:** `GET`
- **Description:** Returns the list of available news categories.
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
- **Description:** Retrieves top headlines from NewsAPI.org.
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

### Supported User Stories

This API directly supports User Story 5 (senior viewing and notifying emergency contacts) and User Story 12 (caregiver managing emergency contacts).

### Get All Emergency Contacts

- **Endpoint:** `/api/v1/emergency-contacts`
- **Method:** `GET`
- **Description:** Retrieves all emergency contacts for the logged-in senior citizen.
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
- **Description:** Retrieves a specific emergency contact by its ID.
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
- **Description:** Updates a specific emergency contact by its ID.
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
- **Description:** Deletes a specific emergency contact by its ID.
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

## Appointments API

Base URL: `/appointments`

### Supported User Stories

This API directly supports User Story 4 (senior viewing upcoming appointments) and User Story 10 (caregiver managing appointments).

### Get All Appointments

- **Endpoint:** `/appointments`
- **Method:** `GET`
- **Description:** Retrieves all appointments.
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
- **Description:** Creates a new appointment.
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
