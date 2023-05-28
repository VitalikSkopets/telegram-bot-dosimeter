import base64

from cryptography.fernet import Fernet

from dosimeter.config import config, settings
from dosimeter.encryption.interface import BaseCryptographer

__all__ = ("SymmetricCryptographer",)


class SymmetricCryptographer(BaseCryptographer):
    """
    A class that encapsulates the logic of encrypting string objects with a
    symmetric method.
    """

    PASSWORD: bytes = bytes(config.enc.pwd, encoding=settings.UTF)

    def __init__(self) -> None:
        key = base64.b64decode(self.PASSWORD)
        self.cipher = Fernet(key)

    def encrypt(self, message: str | None = None) -> str | None:
        """
        Encryption method for string objects.
        """
        if not isinstance(message, str):
            return None
        # encryption
        ciphertext = self.cipher.encrypt(bytes(message, encoding=settings.UTF))
        token = base64.b64encode(ciphertext)
        return token.decode(encoding=settings.UTF)

    def decrypt(self, token: str) -> str | None:
        """
        Method for decrypting string objects.
        """
        if not token or not isinstance(token, str):
            return None
        pre_token = base64.b64decode(token)
        # decryption
        plaintext = self.cipher.decrypt(pre_token)
        return plaintext.decode(encoding=settings.UTF)
