from audit import AuditLogger
from auth import AuthenticationAuthorization, PostureManager
from policy_manager import PolicyManager
from session_management import SessionManager


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
            return "Invalid Request", 403

        # Authenticate the user
        if not self.auth_manager.authenticate(username, password):
            return "Unauthorized", 401

        # Check device posture
        if not self.auth_manager.authorize(username, self.posture_manager):
            return "Posture Invalid", 403

        # Create session
        session_id = self.session_manager.create_session(username)
        
        # Enforce policy
        if self.session_manager.enforce_policy(session_id, self.policy_manager, resource):
            self.audit_logger.log_event(username, f"Access to {resource} granted")
            return "Access Granted", 200
        else:
            self.audit_logger.log_event(username, f"Access to {resource} denied")
            return "Access Denied", 403
