from flask import Flask, request, jsonify
from framework import ZTFramework

app = Flask(__name__)

# Initialize the framework
framework = ZTFramework()

# Route to handle access requests
@app.route('/request_access', methods=['POST'])
def request_access():
    # Extract information from the incoming request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    resource = data.get('resource')
    
    # Request context (can add more details, e.g., IP, device info)
    request_context = {"is_secure": request.is_secure}
    
    # Process the request
    response, status_code = framework.request_access(request_context, username, password, resource)
    return jsonify({'message': response}), status_code

# Other routes for various functions can be added similarly

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Run server with HTTPS (adhoc for local development)
