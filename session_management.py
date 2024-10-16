import secrets

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user):
        session_id = self.generate_session_id()
        self.sessions[session_id] = {"user": user}
        return session_id

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def enforce_policy(self, session_id, policy_manager, resource):
        if session_id in self.sessions:
            user = self.sessions[session_id]['user']
            return policy_manager.evaluate_policy(user, resource)
        return False

    def generate_session_id(self):
        # Use secrets.token_hex() for cryptographically secure session IDs
        return secrets.token_hex(16)  # Generates a 32-character session ID

    def validate_request(self, request):
        return request.get('is_secure', False)
