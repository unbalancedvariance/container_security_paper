import json
from framework import ZTFramework

# Create an instance of the ZTFramework
framework = ZTFramework()

# Mock IP addresses for testing
mock_ips = [
    "192.168.0.1",
    "192.168.0.2",
    "10.0.0.1",
    "172.16.0.1",
    "127.0.0.1"
]

mock_requests = [
    {
        "request": {"is_secure": True},
        "username": "user-1",
        "password": "password-1",
        "resource": "A",
    },
    {
        "request": {"is_secure": True},
        "username": "user-1",
        "password": "password-1",
        "resource": "A",
    },
    {
        "request": {"is_secure": False},
        "username": "user-1",
        "password": "password-1",
        "resource": "resource-1",
    },
    {
        "request": {"is_secure": True},
        "username": "unknown-user",
        "password": "password-1",
        "resource": "resource-1",
    },
    {
        "request": {"is_secure": True},
        "username": "user-1",
        "password": "password-1",
        "resource": "unknown-resource",
    }
]

# Test the framework with mock requests
for i, mock in enumerate(mock_requests):
    request_context = mock['request']
    username = mock['username']
    password = mock['password']
    resource = mock['resource']
    ip_address = mock_ips[i]  # Assign a mock IP for each test case
    
    print(f"Test Case {i + 1}:")
    response, status_code = framework.request_access(request_context, username, password, resource, ip_address)
    print(f"Response: {response}, Status Code: {status_code}\n")
