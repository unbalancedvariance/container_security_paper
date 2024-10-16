from audit import AuditLogger
from auth import AuthenticationAuthorization
from policy_manager import PolicyManager
from session_management import SessionManager
from posture_manager import PostureManager

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
                self.audit_logger.log_event("ZTCF Check -1: Check for Secure connection: Failure (HTTPS connection is mandatory, switch to HTTPS connection and try again)")
                raise ValueError("Secure connection check failed")

            self.audit_logger.log_event("ZTCF Check -1: Check for Secure connection: Success")

            # Authenticate user
            if not self.auth_manager.authenticate(username, password):
                self.audit_logger.log_event("ZTCF Check -2: Check for Valid credentials: Failed")
                raise ValueError("Authentication failed: invalid credentials")

            self.audit_logger.log_event("ZTCF Check -2: Check for Valid credentials: Success")

            # Validate device posture
            if not self.posture_manager.check_posture(username):
                self.audit_logger.log_event("ZTCF Check -3: Check for Valid posture: Failed")
                raise ValueError("Posture validation failed")

            self.audit_logger.log_event("ZTCF Check -3: Check for Valid posture: Success")

            # Enforce policy
            if not self.session_manager.enforce_policy(session_id, self.policy_manager, resource):
                self.audit_logger.log_event("ZTCF Check -4: Check for Valid policy: Failed")
                raise ValueError("Policy enforcement failed")

            self.audit_logger.log_event("ZTCF Check -4: Check for Valid policy: Success")
            self.audit_logger.log_event(f"ZTCF: Access Granted for User \"{username}\"")

            # Log response sent
            self.audit_logger.log_event("ZTCF: Response sent to the user.")
            
            # Trigger continuous monitoring
            self.audit_logger.log_event("ZTCF: Continuous monitoring triggered")

            return "Access granted to resource.", 200

        except ValueError as e:
            # Delete the session if any check fails
            self.session_manager.delete_session(session_id)
            self.audit_logger.log_event(f"ZTCF: Session {session_id} deleted due to failure")
            self.audit_logger.log_event(f"ZTCF: {str(e)} response sent to the user.")
            return str(e), 403
