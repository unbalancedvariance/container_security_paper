class PolicyManager:
    def __init__(self):
        self.policies = {}  # Store policies as {user: {resource: access_rights}}

    def add_policy(self, user, resource, access_rights):
        if user not in self.policies:
            self.policies[user] = {}
        self.policies[user][resource] = access_rights

    def evaluate_policy(self, user, resource):
        return self.policies.get(user, {}).get(resource, False)
