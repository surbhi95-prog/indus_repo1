from cryptography.fernet import Fernet
from django.conf import settings


class PasswordEncryptionService:

    @staticmethod
    def encrypt(password):
        if not password:
            return None

        cipher = Fernet(
            settings.PASSWORD_ENCRYPTION_KEY.encode()
        )

        return cipher.encrypt(
            password.encode()
        ).decode()

    @staticmethod
    def decrypt(encrypted_password):
        if not encrypted_password:
            return None

        cipher = Fernet(
            settings.PASSWORD_ENCRYPTION_KEY.encode()
        )

        return cipher.decrypt(
            encrypted_password.encode()
        ).decode()