from flask import Flask, request, jsonify
from framework import ZTFramework

app = Flask(__name__)

# Initialize the framework
framework = ZTFramework()

# Route to handle access requests
@app.route('/request_access', methods=['POST','GET'])
def request_access():
    # Extract information from the incoming request
    data = request.json
    request_context = {"is_secure": True}
    username = data.get('username')
    password = data.get('password')
    resource = data.get('resource')
    
    # Process the request
    response, status_code = framework.request_access(request_context, username, password, resource)
    return jsonify({'message': response}), status_code


if __name__ == '__main__':
    # app.run(ssl_context='adhoc',port=5050)   # Run server with HTTPS (adhoc for local development)
    app.run(ssl_context=("configuration_files/localhost.pem","configuration_files/localhost-key.pem"),port=5050)  # Run server with HTTPS (adhoc for local development)
