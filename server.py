import os
from flask import Flask, request, jsonify
import argparse
from framework import ZTFramework

app = Flask(__name__)

# Initialize the framework
framework = ZTFramework()


# Define test scenarios
TEST_SCENARIOS = {
    "all_pass": {"username": "user-1", "password": "password-1", "resource": "A","is_secure":True},
    "http_fail": {"username": "user-1", "password": "password-1", "resource": "A","is_secure":False},
    "auth_fail": {"username": "user-1", "password": "password-2", "resource": "B","is_secure":True},
    "policy_fail": {"username": "user-1", "password": "password-1", "resource": "B","is_secure":True},
    "posture_fail": {"username": "user-2", "password": "password-2", "resource": "B","is_secure":True}
}

# Parse command-line argument
parser = argparse.ArgumentParser()
parser.add_argument("--scenario", choices=TEST_SCENARIOS.keys(), help="Select a test scenario")
args, unknown = parser.parse_known_args()

# Get scenario from CLI arg (if provided) or from ENV variable (fallback)
scenario = args.scenario or os.environ.get("TEST_SCENARIO", "all_pass")  # Default: "all_pass"

if scenario not in TEST_SCENARIOS:
    raise ValueError(f"Invalid scenario: {scenario}. Choose from {list(TEST_SCENARIOS.keys())}")

# Route to handle access requests
@app.route('/get_resource', methods=['POST', 'GET'])
def get_resource():
    # Extract information from the incoming request
    # data = request.json
    # request_context = {"is_secure": request.is_secure}  # Check if request is secure (HTTPS)
    # username = data.get('username')
    # password = data.get('password')
    # resource = data.get('resource')
    # ip_address = request.remote_addr

    # based on the test scenario the paramters are selected.
    scenario_data = TEST_SCENARIOS[scenario]
    request_context = {"is_secure": scenario_data["is_secure"]}  # Assume HTTPS for now
    username = scenario_data["username"]
    password = scenario_data["password"]
    resource = scenario_data["resource"]
    ip_address = "192.168.0.1"

    # Process the request with the framework, passing in the request context and IP address
    response, status_code = framework.request_access(request_context, username, password, resource, ip_address)
    # return jsonify({'message': "random response"}), 200
    return jsonify({'message': response}), 200

if __name__ == '__main__':
    # Use HTTPS with self-signed certificates for local development
    app.run(host="0.0.0.0", port=5050, ssl_context="adhoc")  # Change from 127.0.0.1
    # app.run(ssl_context="adhoc", port=5050)
    # app.run(ssl_context=("configuration_files/localhost.pem", "configuration_files/localhost-key.pem"), port=5050)
