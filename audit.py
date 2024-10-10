import logging

class AuditLogger:
    def __init__(self):
        logging.basicConfig(filename='audit.log', level=logging.INFO)

    def log_event(self, user, action):
        logging.info(f"User {user} performed action: {action}")
