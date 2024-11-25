# Travel Microservices Project

## Overview

This project is a microservices-based application designed for managing travel services, including user management, destination management, and authentication. It is composed of several independent microservices, each responsible for specific functionality:

- **User Service**: Handles user registration, login, and profile management.
- **Destination Service**: Manages travel destinations, including adding and deleting destinations (admin-only operations).
- **Authentication Service**: Provides JWT token generation and validation for authentication and authorization.
- **API Gateway**: Serves as a unified entry point to the microservices, forwarding requests to the appropriate service and aggregating API endpoints.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Services](#running-the-services)
- [API Gateway](#api-gateway)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
  - [User Service Endpoints](#user-service-endpoints)
  - [Destination Service Endpoints](#destination-service-endpoints)
  - [Authentication Service Endpoints](#authentication-service-endpoints)
- [Testing the APIs](#testing-the-apis)
- [Data Validation](#data-validation)
- [Security Considerations](#security-considerations)
- [Dependencies](#dependencies)
- [Conclusion](#conclusion)

## Project Structure

The project is organized into multiple microservices, each with its own directory and virtual environment:

```
project/
├── authentication_service/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
├── destination_service/
│   ├── app.py
│   ├── routes.py
│   ├── controllers.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
├── user_service/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
├── gateway/
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
├── .env
└── README.md
```

- **Authentication Service** (port 5003)
- **User Service** (port 5002)
- **Destination Service** (port 5001)
- **API Gateway** (port 5000)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (venv or virtualenv)

## Installation

### Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/arman-007/assignment-5.git
cd assignment-5
```

### Create Virtual Environment


#### Linux/macOS

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following environment variables:

```env
# .env
DESTINATION_SERVICE_URL=http://localhost:5001
USER_SERVICE_URL=http://localhost:5002
AUTHENTICATION_SERVICE_URL=http://localhost:5003
SECRET_KEY=your_secret_key
```

These variables are required for the services to communicate and for security configurations.

## Running the Services

To run the services, open separate terminal windows for each service, activate their respective virtual environments, and run the following commands:

1. **Authentication Service**

   ```sh
   cd authentication_service
   python run.py
   ```

2. **User Service**

   ```sh
   cd user_service
   python run.py
   ```

3. **Destination Service**

   ```sh
   cd destination_service
   python run.py
   ```

4. **API Gateway**

   ```sh
   cd gateway
   python app.py
   ```

## API Gateway

The API Gateway acts as a unified entry point for all the microservices. All requests pass through the gateway, which forwards them to the appropriate service.

- **Base URL**: `http://localhost:5000`

## API Documentation

Each microservice provides its own Swagger documentation, typically accessible at `/swagger.json` or `/docs`. To aggregate API documentation in a single interface, additional configuration is required (not covered here).

## API Endpoints

### User Service Endpoints

- **Register a New User**
  - **Endpoint**: `POST /api/users/users/register`
  - **Description**: Registers a new user.
  - **Payload**:
    ```json
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "password": "password123",
      "role": "User"
    }
    ```
  - **Responses**:
    - `201 Created`: User successfully registered.
    - `400 Bad Request`: Invalid input or user already exists.

- **Login**
  - **Endpoint**: `POST /api/users/users/login`
  - **Description**: Authenticates a user and returns a JWT token.
  - **Payload**:
    ```json
    {
      "email": "john.doe@example.com",
      "password": "password123"
    }
    ```
  - **Responses**:
    - `200 OK`: Login successful, returns token.
    - `400 Bad Request`: Invalid input.
    - `401 Unauthorized`: Invalid email or password.

- **Get User Profile**
  - **Endpoint**: `GET /api/users/users/profile`
  - **Description**: Retrieves the profile information of the authenticated user.
  - **Headers**: `Authorization: Bearer <token>`
  - **Responses**:
    - `200 OK`: Returns user's profile.
    - `401 Unauthorized`: Token is missing or invalid.
    - `404 Not Found`: User not found.

### Destination Service Endpoints

- **Get All Destinations**
  - **Endpoint**: `GET /api/destinations/destinations/destinations`
  - **Description**: Retrieves a list of all destinations.
  - **Responses**:
    - `200 OK`: Returns list of destinations.

- **Add a New Destination (Admin Only)**
  - **Endpoint**: `POST /api/destinations/destinations/destination`
  - **Description**: Adds a new destination. Only accessible by admin users.
  - **Headers**: `Authorization: Bearer <token>`
  - **Payload**:
    ```json
    {
      "name": "Paris",
      "description": "The City of Light",
      "location": "France"
    }
    ```
  - **Responses**:
    - `201 Created`: Destination added successfully.
    - `400 Bad Request`: Invalid input.
    - `401 Unauthorized`: Token is missing or invalid.
    - `403 Forbidden`: Admin access required.

- **Delete a Destination (Admin Only)**
  - **Endpoint**: `DELETE /api/destinations/destinations/destinations/<id>`
  - **Description**: Deletes a destination by ID. Only accessible by admin users.
  - **Headers**: `Authorization: Bearer <token>`
  - **Responses**:
    - `200 OK`: Destination deleted successfully.
    - `401 Unauthorized`: Token is missing or invalid.
    - `403 Forbidden`: Admin access required.
    - `404 Not Found`: Destination not found.

### Authentication Service Endpoints

- **Generate Token**
  - **Endpoint**: `POST /api/auth/auth/token`
  - **Description**: Generates a JWT token for a user.
  - **Payload**:
    ```json
    {
      "email": "john.doe@example.com",
      "role": "User"
    }
    ```
  - **Responses**:
    - `200 OK`: Returns token.
    - `400 Bad Request`: Invalid input.

- **Validate Token**
  - **Endpoint**: `POST /api/auth/auth/validate`
  - **Description**: Validates a JWT token.
  - **Headers**: `Authorization: Bearer <token>`
  - **Responses**:
    - `200 OK`: Token is valid.
    - `401 Unauthorized`: Token is missing or invalid.

## Testing the APIs

You can test the APIs using tools like **Postman**, **cURL**, or any REST client.

### Example Workflow

1. **Register a New User**: Create a new user using the `/register` endpoint.
2. **Login**: Authenticate the user and receive a token using the `/login` endpoint.
3. **Add a New Destination**: Use the token to add a new destination (admin-only operation).
4. **Get All Destinations**: Retrieve a list of all destinations.
5. **Delete a Destination**: Use the token to delete a destination (admin-only operation).

## Data Validation

All incoming request data is validated using **Pydantic** models to ensure data integrity and consistency. If validation fails, a `400 Bad Request` is returned with error details.

### Example Pydantic Model

Here is an example of a Pydantic model used for user registration in `user_service/models.py`:

```python
from pydantic import BaseModel, EmailStr, constr

class UserRegistrationModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    password: constr(min_length=6)
    role: constr(strip_whitespace=True)
```

## Security Considerations

- **JWT Tokens**: Used for authentication and authorization.
- **Admin-Only Endpoints**: Certain endpoints require admin privileges.
- **Password Hashing**: Passwords are stored using `werkzeug.security.generate_password_hash` to ensure security.
- **Input Validation**: All input data is validated to prevent injection attacks.
- **HTTPS**: In production, it's recommended to use HTTPS to secure communication.

## Dependencies

Key dependencies include:

- **Flask**: Web framework for building APIs.
- **Flask-RESTX**: Extension for building REST APIs.
- **Pydantic**: Data validation and settings management.
- **Python-Dotenv**: Loads environment
