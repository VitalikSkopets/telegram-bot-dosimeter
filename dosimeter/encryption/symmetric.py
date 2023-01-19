import base64

from cryptography.fernet import Fernet

from dosimeter.config import PWD
from dosimeter.encryption.interface import BaseCryptographer

__all__ = ("SymmetricCryptographer", "cryptographer")


class SymmetricCryptographer(BaseCryptographer):
    PASSWORD: bytes = bytes(PWD, encoding="utf-8")

    def __init__(self) -> None:
        key = base64.b64decode(self.PASSWORD)
        self.cipher = Fernet(key)

    def encrypt(self, message: str | None = None) -> str | None:
        if not isinstance(message, str):
            return None
        # encryption
        ciphertext = self.cipher.encrypt(bytes(message, encoding="utf-8"))
        token = base64.b64encode(ciphertext)
        return token.decode(encoding="utf-8")

    def decrypt(self, token: str) -> str | None:
        if not token or not isinstance(token, str):
            return None
        pre_token = base64.b64decode(token)
        # decryption
        plaintext = self.cipher.decrypt(pre_token)
        return plaintext.decode(encoding="utf-8")


"""SymmetricCryptographer class instance"""
cryptographer = SymmetricCryptographer()

if __name__ == "__main__":

    enc_rtext = cryptographer.encrypt("Test string")
    print(f"Encrypted string: {enc_rtext}")

    plain_text = cryptographer.decrypt(
        token="Z0FBQUFBQmp5WVFSelUtaWdqRXN5MHdKenlGc1NYQ2RDYUctMTNtWC16UFdVRHhab2NGR2l"
        "jaFBhR2NKV1pUWTJKbVdyM21WblJFODM4VTMwWFdod1lNS3hnRWRlVENJbGc9PQ== "
    )
    print(f"Decrypted string: {plain_text}")