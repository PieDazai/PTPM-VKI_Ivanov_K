import hashlib

from src import validation_register

class RegistrationService:

    def hash_password(self, password):

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        return password_hash

    def register(
            self,
            login,
            password,
            confirm_password
    ):
        return validation_register.register_user(
            login,
            password,
            confirm_password
        )