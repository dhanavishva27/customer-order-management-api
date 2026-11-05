# Customer and Order Management REST API

## Project Overview

A REST API developed using Python FastAPI and MySQL to manage customers and their orders. The application supports CRUD operations, JWT authentication, input validation, error handling, and API consumption through a Python client.

## Technologies Used

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Python Requests

## Database Tables

**customers:** id, name, email, phone, created_at

**orders:** id, customer_id, order_number, amount, status, created_at

Relationship: One customer can have multiple orders.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/login | Authenticate and generate JWT |
| POST | /api/customers | Create customer |
| GET | /api/customers | Retrieve customers |
| GET | /api/customers/{id} | Retrieve customer by ID |
| PUT | /api/customers/{id} | Update customer |
| DELETE | /api/customers/{id} | Delete customer |
| POST | /api/orders | Create order |
| GET | /api/orders | Retrieve orders |
| GET | /api/customers/{id}/orders | Retrieve customer orders |
| GET | /api/customers/{id}/summary | Retrieve customer order summary |

## Installation and Setup

1. Install Python and MySQL.
2. Create the MySQL database using schema.sql.
3. Create and activate a Python virtual environment.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Create a `.env` file with the following configuration:

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=customer_order_db

   AUTH_USERNAME=admin
   AUTH_PASSWORD=your_login_password
   JWT_SECRET_KEY=your_random_secret_key
   ```

6. Start the FastAPI server:

   `uvicorn app.main:app --reload`

7. Open Swagger documentation:

   `http://127.0.0.1:8000/docs`

8. Run the Python API client:

   `python client.py`

## Authentication

The login API generates a JWT access token. Protected endpoints require the token in the Authorization header using the Bearer authentication scheme.

## Error Handling

The API uses HTTP status codes including:

- 200 — Successful request
- 201 — Resource created
- 204 — Resource deleted
- 401 — Unauthorized
- 404 — Resource not found
- 409 — Database relationship conflict
- 422 — Request validation failed

## API Consumption

The `client.py` script demonstrates logging in, creating customers, retrieving customers, creating orders, fetching customer orders, updating customers, deleting customers, and handling API errors.

## Customer Summary

The summary endpoint calculates the total number of orders, total order amount, completed orders, and pending orders for a specific customer.
