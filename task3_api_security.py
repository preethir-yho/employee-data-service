import os
import requests
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


# 2. Create API session with retry logic
session = requests.Session()

retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)


# 3. Get employee data from API
def get_users():
    url = "https://jsonplaceholder.typicode.com/users"

    response = session.get(url)
    response.raise_for_status()

    users = response.json()

    for user in users[:5]:
        print(f'{user.get("id")} - ' f'{user.get("name")} - ' f'{user.get("email")}')

    return users


# 4. Display nested JSON data
def show_user_details(user):
    address = user.get("address", {})
    geo = address.get("geo", {})
    company = user.get("company", {})

    city = address.get("city", "Not Available")
    zip_code = address.get("zipcode", "Not Available")
    latitude = geo.get("lat", "Not Available")
    company_name = company.get("name", "Not Available")

    print(f"City: {city} | Zip: {zip_code}")
    print(f"Latitude: {latitude}")
    print(f"Company: {company_name}")


# 5. Verify webhook signature using HMAC
def verify_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


# MAIN PROGRAM
if __name__ == "__main__":

    # Check environment variables
    if not API_KEY or not WEBHOOK_SECRET:
        print("Environment variables are missing!")
        exit()

    # Get users from API
    users = get_users()

    print("\nFirst user's details:")
    show_user_details(users[0])

    # Webhook testing
    payload = '{"employee_id": 101, "action": "created"}'

    # Generate a valid signature
    valid_signature = hmac.new(
        WEBHOOK_SECRET.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    # Test valid signature
    valid = verify_signature(payload, valid_signature, WEBHOOK_SECRET)

    # Test tampered payload
    tampered = verify_signature(
        '{"employee_id": 102, "action": "created"}', valid_signature, WEBHOOK_SECRET
    )

    # Test wrong secret
    wrong_secret = verify_signature(payload, valid_signature, "wrong_secret")

    print("\nWebhook Results:")
    print(
        f"Valid: {valid} | " f"Tampered: {tampered} | " f"Wrong secret: {wrong_secret}"
    )
