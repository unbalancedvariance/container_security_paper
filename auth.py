# main.py
from cryptography.fernet import Fernet
import json
import os
from posture_manager import PostureManager

class AuthenticationAuthorization:
    def __init__(self, credentials_file="configuration_files/credentials.json", key_file="configuration_files/secret.key"):
        self.credentials_file = credentials_file
        self.key_file = key_file
        self.cipher = self.load_key()

    def load_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()

        return Fernet(key)

    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def store_credentials(self, username, password):
        encrypted_password = self.encrypt_data(password)
        credentials = {}
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as file:
                credentials = json.load(file)
        # Store the plain username and encrypted password
        credentials[username] = encrypted_password
        with open(self.credentials_file, 'w') as file:
            json.dump(credentials, file)

    def authenticate(self, username, password):
        if not os.path.exists(self.credentials_file):
            return False

        with open(self.credentials_file, 'r') as file:
            credentials = json.load(file)

        encrypted_password = credentials.get(username, None)  # Lookup by plain username

        if encrypted_password:
            decrypted_password = self.decrypt_data(encrypted_password)
            return decrypted_password == password

        return False

    def authorize(self, user, posture_manager):
        return posture_manager.check_posture(user)


# if __name__ == "__main__":
#     auth = AuthenticationAuthorization()

#     # Store new credentials (encrypted)
#     auth.store_credentials("user-1", "password-1")
#     auth.store_credentials("user-2", "password-2")

#     # Authenticate a user
#     is_authenticated = auth.authenticate("user-1", "password-1")
#     print(f"Authentication successful: {is_authenticated}")

#     # Posture check and authorization
#     posture_manager = PostureManager()
#     is_authorized = auth.authorize("user-1", posture_manager)
#     print(f"Authorization successful: {is_authorized}")
