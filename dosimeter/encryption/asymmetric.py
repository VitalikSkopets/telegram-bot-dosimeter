import base64
import pathlib
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from dosimeter.config import UTF, config
from dosimeter.encryption.interface import BaseCryptographer


class AsymmetricCryptographer(BaseCryptographer):
    """
    A class that encapsulates the logic of encrypting string objects using an
    asymmetric method.
    """

    PASSWORD: bytes = bytes(config.enc.pwd, encoding=UTF)
    PRIV_KEY: pathlib.Path = config.enc.key.SECRET
    PUB_KEY: pathlib.Path = config.enc.key.PUBLIC

    def __init__(self) -> None:
        if pathlib.Path(self.PRIV_KEY and self.PUB_KEY).exists():
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
        with open(self.PRIV_KEY, "wb") as key_file:
            key_file.write(priv_pem)

        # writing to a public key file
        with open(self.PUB_KEY, "wb") as key_file:
            key_file.write(pub_pem)

    def encrypt(self, message: str | None = None) -> str | None:
        """
        Encryption method for string objects.
        """
        if not isinstance(message, str):
            return None
        # downloading from a public key file
        with open(self.PUB_KEY, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
            )
        # encryption
        assert isinstance(public_key, RSAPublicKey)
        ciphertext: Any = public_key.encrypt(
            bytes(message, encoding=UTF),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        token = base64.b64encode(ciphertext)
        return token.decode(encoding=UTF)

    def decrypt(self, token: str) -> str | None:
        """
        Method for decrypting string objects.
        """
        if not token or not isinstance(token, str):
            return None
        # downloading from a secret key file
        with open(self.PRIV_KEY, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=self.PASSWORD,
            )
        pre_token = base64.b64decode(token)
        # decryption
        assert isinstance(private_key, RSAPrivateKey)
        plaintext = private_key.decrypt(
            pre_token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode(encoding=UTF)
