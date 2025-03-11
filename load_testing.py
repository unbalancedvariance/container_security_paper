import requests
import time

# Server URL
SERVER_URL = "https://localhost:5050/get_resource"

# Number of requests to send
NUM_REQUESTS = 100

# Disable SSL warnings for self-signed certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for i in range(NUM_REQUESTS):
    try:
        response = requests.get(SERVER_URL, verify=False)
        print(f"Request {i+1}: Status {response.status_code}, Response {response.json()}")
    except Exception as e:
        print(f"Request {i+1}: Error {e}")
    time.sleep(0.1)  # Optional: Add a small delay between requests
