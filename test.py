import json
from framework import ZTFramework

# Create an instance of the ZTFramework
framework = ZTFramework()

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
    
    print(f"Test Case {i + 1}:")
    response, status_code = framework.request_access(request_context, username, password, resource)
    print(f"Response: {response}, Status Code: {status_code}\n")
