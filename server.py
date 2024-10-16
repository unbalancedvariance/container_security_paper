from flask import Flask, request, jsonify
from framework import ZTFramework

app = Flask(__name__)

# Initialize the framework
framework = ZTFramework()

# Route to handle access requests
@app.route('/request_access', methods=['POST', 'GET'])
def request_access():
    # Extract information from the incoming request
    data = request.json
    request_context = {"is_secure": request.is_secure}  # Check if request is secure (HTTPS)
    username = data.get('username')
    password = data.get('password')
    resource = data.get('resource')
    
    # Get the client's IP address
    ip_address = request.remote_addr

    # Process the request with the framework, passing in the request context and IP address
    response, status_code = framework.request_access(request_context, username, password, resource, ip_address)
    
    return jsonify({'message': response}), status_code


if __name__ == '__main__':
    # Use HTTPS with self-signed certificates for local development
    app.run(ssl_context=("configuration_files/localhost.pem", "configuration_files/localhost-key.pem"), port=5050)
