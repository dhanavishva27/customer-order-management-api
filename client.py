import os
import requests
from dotenv import load_dotenv

# Load login credentials from .env
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

USERNAME = os.getenv("AUTH_USERNAME")
PASSWORD = os.getenv("AUTH_PASSWORD")

session = requests.Session()


def send_request(method, endpoint, **kwargs):
    """Send an HTTP request and handle API errors."""

    url = BASE_URL + endpoint

    try:
        response = session.request(method, url, **kwargs)

        print(f"\n{method} {endpoint} -> {response.status_code}")

        response.raise_for_status()

        # DELETE may return 204 with no response body
        if response.status_code == 204:
            print("Operation completed successfully.")
            return None

        result = response.json()
        print(result)
        return result

    except requests.exceptions.HTTPError as error:
        print("API error:", error.response.status_code)
        print(error.response.text)
        raise

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)
        raise


def main():

    # 1. Login and obtain JWT token
    print("\n--- LOGIN ---")

    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    result = send_request("POST", "/api/login", json=login_data)

    token = result["access_token"]

    # Attach token to all subsequent requests
    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    print("Login successful. JWT token received.")

    # 2. Create a customer
    print("\n--- CREATE CUSTOMER ---")

    customer_data = {
        "name": "Arun Kumar",
        "email": "arun@example.com",
        "phone": "9876543210"
    }

    result = send_request(
        "POST",
        "/api/customers",
        json=customer_data
    )

    customer_id = result["data"]["id"]

    # 3. Fetch all customers
    print("\n--- GET ALL CUSTOMERS ---")

    send_request("GET", "/api/customers")

    # 4. Create an order for the customer
    print("\n--- CREATE ORDER ---")

    order_data = {
        "customer_id": customer_id,
        "order_number": "ORD-1001",
        "amount": 2500.00,
        "status": "completed"
    }

    send_request(
        "POST",
        "/api/orders",
        json=order_data
    )

    # 5. Fetch orders belonging to this customer
    print("\n--- GET CUSTOMER ORDERS ---")

    send_request(
        "GET",
        f"/api/customers/{customer_id}/orders"
    )

    # 6. Update the customer
    print("\n--- UPDATE CUSTOMER ---")

    updated_customer = {
        "name": "Arun Kumar",
        "email": "arun.updated@example.com",
        "phone": "9876501234"
    }

    send_request(
        "PUT",
        f"/api/customers/{customer_id}",
        json=updated_customer
    )

    # 7. Create a separate customer for deletion
    print("\n--- CREATE CUSTOMER FOR DELETE TEST ---")

    temporary_customer = {
        "name": "Temporary Customer",
        "email": "temporary@example.com",
        "phone": "9000000000"
    }

    result = send_request(
        "POST",
        "/api/customers",
        json=temporary_customer
    )

    temporary_customer_id = result["data"]["id"]

    # 8. Delete the temporary customer
    print("\n--- DELETE CUSTOMER ---")

    send_request(
        "DELETE",
        f"/api/customers/{temporary_customer_id}"
    )


if __name__ == "__main__":
    try:
        main()
    except (requests.exceptions.RequestException, KeyError, TypeError) as error:
        print("\nClient execution stopped:", error) 