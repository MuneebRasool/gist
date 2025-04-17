"""Utility for encryption and decryption of sensitive data."""

from cryptography.fernet import Fernet
from src.config.settings import SECRET_KEY


class Encryption:
    """Class for handling encryption and decryption."""

    def __init__(self):
        import base64

        key = base64.urlsafe_b64encode(SECRET_KEY.encode().ljust(32)[:32])
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        """
        Encrypt the data.
        Args:
            data: String to encrypt
        Returns:
            str: Encrypted data in base64 format
        """
        if not data:
            return None
        encrypted_data = self.cipher.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt the data.
        Args:
            encrypted_data: Encrypted string in base64 format
        Returns:
            str: Decrypted data
        """
        if not encrypted_data:
            return None
        decrypted_data = self.cipher.decrypt(encrypted_data.encode())
        return decrypted_data.decode()


encryption = Encryption()
