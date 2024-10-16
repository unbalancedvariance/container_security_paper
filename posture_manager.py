# posture_manager.py
import json
import os

class PostureManager:
    def __init__(self, posture_file='configuration_files/postures.json'):
        self.posture_file = posture_file
        self.postures = self.load_postures()

    def load_postures(self):
        # Load postures from a JSON file
        if os.path.exists(self.posture_file):
            with open(self.posture_file, 'r') as file:
                return json.load(file)
        return {}

    def check_posture(self, user):
        # Validate user's posture (e.g., device, IP, location)
        if user not in self.postures:
            print(f"No posture information for {user}")
            return False
        
        user_posture = self.postures[user]

        # Mock posture validation!
        if user_posture['device'] == 'laptop' and user_posture['location'] == 'office':
            return True
        else:
            print(f"Posture validation failed for {user}: {user_posture}")
            return False
