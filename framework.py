from flask import jsonify
from audit import AuditLogger
from auth import AuthenticationAuthorization
from policy_manager import PolicyManager
from session_management import SessionManager
from posture_manager import PostureManager
import json

class ZTFramework:
    def __init__(self):
        self.session_manager = SessionManager()
        self.auth_manager = AuthenticationAuthorization()
        self.policy_manager = PolicyManager()
        self.audit_logger = AuditLogger()
        self.posture_manager = PostureManager()

    def request_access(self, request, username, password, resource, ip_address):
        # Log initial request
        self.audit_logger.log_event("ZTCF: User request received in the ZTCF test container")

        # Create session before any checks
        session_id = self.session_manager.create_session(username)
        self.audit_logger.log_event(f"ZTCF: User session created for user \"{username}\", ip address: \"{ip_address}\", user session id: {session_id}")

        try:
            # Validate request (e.g., HTTPS)
            if not request.get('is_secure', False):
                self.audit_logger.log_event("ZTCF Check -1: Check for Secure connection: Failed (Non-HTTPS connection detected)")
                raise ValueError("Access denied: A secure HTTPS connection is required. Please switch to HTTPS and try again.")

            self.audit_logger.log_event("ZTCF Check -1: Check for Secure connection: Success")

            # Authenticate user
            if not self.auth_manager.authenticate(username, password):
                self.audit_logger.log_event("ZTCF Check -2: Check for Valid credentials: Failed")
                raise ValueError("Access denied: Invalid credentials. Please check your username and password and try again.")

            self.audit_logger.log_event("ZTCF Check -2: Check for Valid credentials: Success")

            # Validate device posture
            if not self.posture_manager.check_posture(username):
                self.audit_logger.log_event("ZTCF Check -3: Check for Valid posture: Failed")
                raise ValueError("Access denied: Device posture validation failed. Please ensure your device meets security requirements.")

            self.audit_logger.log_event("ZTCF Check -3: Check for Valid posture: Success")

            # Enforce policy
            if not self.session_manager.enforce_policy(session_id, self.policy_manager, resource):
                self.audit_logger.log_event("ZTCF Check -4: Check for Valid policy: Failed")
                raise ValueError("Access denied: You do not have permission to access this resource according to enforced policy.")

            self.audit_logger.log_event("ZTCF Check -4: Check for Valid policy: Success")
            self.audit_logger.log_event(f"ZTCF: Access granted for User \"{username}\"")

            # Load and return the mock resource
            with open('resource.json', 'r') as file:
                resource_data = json.load(file)

            # Log response sent
            self.audit_logger.log_event("ZTCF: Response sent to the user.")
                        
            # Trigger continuous monitoring
            self.audit_logger.log_event("ZTCF: Continuous monitoring triggered")

            # Return the resource data directly (as a dictionary)
            return resource_data, 200


        except ValueError as e:
            # Delete the session if any check fails
            self.session_manager.delete_session(session_id)
            self.audit_logger.log_event(f"ZTCF: Session {session_id} deleted due to failure")
            self.audit_logger.log_event(f"ZTCF: {str(e)} response sent to the user.")
            
            # Return a proper JSON response
            return {"error": str(e)}, 403

