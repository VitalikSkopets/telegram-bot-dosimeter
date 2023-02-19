import base64
import pathlib
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from dosimeter.config import PWD
from dosimeter.constants import Files
from dosimeter.encryption.interface import BaseCryptographer

__all__ = ("AsymmetricCryptographer",)


class AsymmetricCryptographer(BaseCryptographer):
    """A class that encapsulates the logic of encrypting string objects using an
    asymmetric method."""

    PASSWORD: bytes = bytes(PWD, encoding="utf-8")
    PRIV_KEY_PATH: pathlib.Path = Files.SECRET_KEY
    PUB_KEY_PATH: pathlib.Path = Files.PUBLIC_KEY

    def __init__(self) -> None:
        if pathlib.Path(self.PRIV_KEY_PATH and self.PUB_KEY_PATH).exists():
            return
        # creating a private (secret) key
        private_key: RSAPrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # creating a public key based on a secret key
        public_key: RSAPublicKey = private_key.public_key()

        # serialization of the secret key
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(self.PASSWORD),
        )

        # public key serialization
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # writing to the secret key file
        with open(self.PRIV_KEY_PATH, "wb") as key_file:
            key_file.write(priv_pem)

        # writing to a public key file
        with open(self.PUB_KEY_PATH, "wb") as key_file:
            key_file.write(pub_pem)

    def encrypt(self, message: str | None = None) -> str | None:
        """Encryption method for string objects."""
        if not isinstance(message, str):
            return None
        # downloading from a public key file
        with open(self.PUB_KEY_PATH, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
            )
        # encryption
        ciphertext: Any = public_key.encrypt(  # type: ignore[union-attr]
            bytes(message, encoding="utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        token = base64.b64encode(ciphertext)
        return token.decode(encoding="utf-8")

    def decrypt(self, token: str) -> str | None:
        """Method for decrypting string objects."""
        if not token or not isinstance(token, str):
            return None
        # downloading from a secret key file
        with open(self.PRIV_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=self.PASSWORD,
            )
        pre_token = base64.b64decode(token)
        # decryption
        plaintext = private_key.decrypt(  # type: ignore[union-attr]
            pre_token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode(encoding="utf-8")


if __name__ == "__main__":
    cryptographer = AsymmetricCryptographer()
    enc_text = cryptographer.encrypt("Test string")
    # print(f"Encrypted string: {enc_text}")

    plain_text = cryptographer.decrypt(
        token="ApQnpEss/FJNWK7ImDH8vHLVgblCgbAVjBMnkIcDQZGJ4hZkhw6MFEWkATa/bG7"
        "+T0kGFV5S8+fGukJgZEq15ZnwwOMxt1CPh5y7eV9sTfXPjnRtaoHb9z/El2pdW2"
        "+Fd5rYwJtNsS7hE5O7uqwxLbE2AlbdfE46WG7Rqz5v94BEi+I7cXzJfnU37ryB2Y"
        "+zsUijypRVe4CeUgNXXYL9N4+BuKpFmE5MtRpXSgBZtwddGH643Sq+s"
        "+FfplQN7HJ6JZXoi/p/wWgZXIyfEZxbY+DVkdlFJaTp0nYIKHMNqj+H7emj1dxx4wvzam"
        "+h4aPzz2iPfWymt66Up0FM6TyPTA== "
    )
    # print(f"Decrypted string: {plain_text}")
