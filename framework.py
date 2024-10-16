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

    def request_access(self, request, username, password, resource):
        # Validate the request (e.g., HTTPS, encrypted)
        if not self.session_manager.validate_request(request):
            self.audit_logger.log_event(username, "Authentication failed: secure HTTPS connection is required. Please ensure the connection is over HTTPS and try again.")
            return "Authentication failed: secure HTTPS connection is required. Please ensure the connection is over HTTPS and try again.", 403
        else:
            self.audit_logger.log_event(username, "Request validation successful.")

        # # Authenticate the user
        if not self.auth_manager.authenticate(username, password):
            self.audit_logger.log_event(username, "Authentication failed because of Invalid Credentials.")
            return "Authentication failed because of Invalid Credentials.", 401
        else:
            self.audit_logger.log_event(username, "Authentication successful.")

        # # Validate device posture using the posture manager
        if not self.posture_manager.check_posture(username):
            self.audit_logger.log_event(username, "Posture validation failed")
            return "Access Denied because of Invalid Posture.Please try reconnecting!", 403
        else:
            self.audit_logger.log_event(username, "Posture validation successful.")

        # # Create session
        session_id = self.session_manager.create_session(username)
        self.audit_logger.log_event(username, f"Session {session_id} created.")
        
        if self.session_manager.enforce_policy('session_id', self.policy_manager, resource):
            self.audit_logger.log_event(username, f"Access to {resource} granted")
            return "Access Granted, You can now access the resource!", 200
        else:
            self.audit_logger.log_event(username, f"Access to {resource} denied due to Enforced Policy.Please Try reconnecting!")
            return "Access Denied due to Enforced policy.", 403
