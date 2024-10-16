import configparser
import os
import json

class PolicyManager:
    def __init__(self, config_file="configuration_files/policies.conf", posture_file="configuration_files/postures.json"):
        self.policies = {}  # Store policies as {user: {resource: access_rights}}
        config_file_path = os.path.join(os.path.dirname(__file__), config_file)  # Get absolute path
        self.posture_file_path = os.path.join(os.path.dirname(__file__), posture_file)  # Get absolute path for posture file
        self.load_policies(config_file_path)

    def load_policies(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Read each section (representing a user) and load their policies
        for user in config.sections():
            resource = config[user].get('resource')
            location = config[user].get('location')
            self.add_policy(user, resource, location)

    def add_policy(self, user, resource, access_rights):
        if user not in self.policies:
            self.policies[user] = {}
        self.policies[user][resource] = access_rights

    def load_posture_data(self):
        # Load posture data from the JSON file
        if os.path.exists(self.posture_file_path):
            with open(self.posture_file_path, 'r') as file:
                return json.load(file)
        return {}

    def evaluate_policy(self, user, resource):
        # Load posture data
        posture_data = self.load_posture_data()

        # Get the location of the user from the posture data
        user_location = posture_data.get(user, {}).get('location', None)

        # Evaluate if the user has access to the resource in the specific location
        access_rights = self.policies.get(user, {}).get(resource, None)
        if access_rights and access_rights == user_location:
            return True
        return False


if __name__ == "__main__":
    policy_manager = PolicyManager()

    # Evaluate policy for UserA and resource A
    print(policy_manager.evaluate_policy('user-1', 'A'))  
    print(policy_manager.evaluate_policy('user-2', 'B'))  
    print(policy_manager.evaluate_policy('user-1', 'B')) 
