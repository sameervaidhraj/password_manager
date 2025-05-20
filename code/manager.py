import hashlib
import base64
import pickle
import os
from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self, master_password=None):
        self.master_password = master_password
        self.key = None
        self.data = {}
        if master_password:
            self.key = self.generate_key(master_password)
        self.load_master_password()
        self.load_data()

    def load_master_password(self):
        """Load the stored master password from a file if available."""
        if os.path.exists('master_password.pickle'):
            with open('master_password.pickle', 'rb') as f:
                stored_password = pickle.load(f)
                # Validate if the entered password matches the stored one
                if self.master_password != stored_password:
                    raise ValueError("Incorrect master password.")
                self.key = self.generate_key(self.master_password)
        else:
            self.setup_master_password()

    def setup_master_password(self):
        """Prompt user to set a new master password if it's the first time."""
        if not self.master_password:
            raise ValueError("Master password not set.")
        self.key = self.generate_key(self.master_password)
        with open('master_password.pickle', 'wb') as f:
            pickle.dump(self.master_password, f)
        print("Master password set successfully.")

    def generate_key(self, password):
        """Generate a 32-byte key suitable for Fernet using SHA256 hash of the password."""
        hash = hashlib.sha256(password.encode()).digest()
        key = base64.urlsafe_b64encode(hash[:32])  # Take the first 32 bytes and encode them in base64
        return key

    def add_password(self, site, username, password):
        encrypted_site = self.encrypt_data(site)
        encrypted_username = self.encrypt_data(username)
        encrypted_password = self.encrypt_data(password)

        self.data[encrypted_site] = {
            'username': encrypted_username,
            'password': encrypted_password,
        }
        self.save_data()

    def delete_password(self, site):
        encrypted_site = self.encrypt_data(site)
        if encrypted_site in self.data:
            del self.data[encrypted_site]
            self.save_data()

    def get_password(self, site):
        encrypted_site = self.encrypt_data(site)
        if encrypted_site in self.data:
            return self.data[encrypted_site]
        return None

    def encrypt_data(self, data):
        """Encrypt any string data using Fernet."""
        f = Fernet(self.key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypt encrypted data using Fernet."""
        f = Fernet(self.key)
        decrypted_data = f.decrypt(encrypted_data).decode()
        return decrypted_data

    def save_data(self):
        with open('password_data.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open('password_data.pickle', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def reset_master_password(self, old_password, new_password):
        """Reset the master password if the old password is correct."""
        if old_password == self.master_password:
            self.master_password = new_password
            self.key = self.generate_key(new_password)
            with open('master_password.pickle', 'wb') as f:
                pickle.dump(self.master_password, f)
            print("Master password has been reset.")
        else:
            raise ValueError("Incorrect old master password.")
