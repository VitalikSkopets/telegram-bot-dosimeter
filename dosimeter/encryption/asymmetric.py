import base64
import pathlib
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from dosimeter.config import PWD
from dosimeter.constants import Files
from dosimeter.encryption.interface import BaseCryptographer

__all__ = ("AsymmetricCryptographer", "cryptographer")


class AsymmetricCryptographer(BaseCryptographer):
    PASSWORD: bytes = bytes(PWD, encoding="utf-8")
    PRIV_KEY_PATH: pathlib.Path = Files.SECRET_KEY
    PUB_KEY_PATH: pathlib.Path = Files.PUBLIC_KEY

    def __init__(self) -> None:
        if pathlib.Path(self.PRIV_KEY_PATH and self.PUB_KEY_PATH).exists():
            return
        # создание закрытого (секретного) ключа
        private_key: RSAPrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # создание публичного (открытого) ключа на основе секретного ключа
        public_key: RSAPublicKey = private_key.public_key()

        # сериализация секретного ключа
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(self.PASSWORD),
        )

        # сериализация открытого ключа
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # запись в файл секретного ключа
        with open(self.PRIV_KEY_PATH, "wb") as key_file:
            key_file.write(priv_pem)

        # запись в файл открытого ключа
        with open(self.PUB_KEY_PATH, "wb") as key_file:
            key_file.write(pub_pem)

    def encrypt(self, message: str | None = None) -> str | None:
        if not isinstance(message, str):
            return None
        # загрузка из файла открытого ключа
        with open(self.PUB_KEY_PATH, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
            )
        # шифрование
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
        if not token or not isinstance(token, str):
            return None
        # загрузка из файла секретного ключа
        with open(self.PRIV_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=self.PASSWORD,
            )
        pre_token = base64.b64decode(token)
        # дешифрование
        plaintext = private_key.decrypt(  # type: ignore[union-attr]
            pre_token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode(encoding="utf-8")


"""AsymmetricCryptographer class instance"""
cryptographer = AsymmetricCryptographer()

if __name__ == "__main__":
    enc_text = cryptographer.encrypt("Test string")
    print(f"Encrypted string: {enc_text}")

    plain_text = cryptographer.decrypt(
        token="YX9dd/pNhcOAd8rRyvpdm"
        "+3t8Rf1GCq0EufwFt7TrBW3Bziv6lFCBz1JWcmbD2UXaei0aCOpqrwn1npj7DIjn"
        "/wvNINGjPxQTEFFCDenR/io++V0BJlQEG1zm1LiGfqcGFqdmMCIeY8"
        "/+xAvlwHYEj9XicbhmmbObdlN"
        "/RbYUVI0UcfCFMaIHAFniOGh3GO2ETg7j7W9TueFlR23DZf4Z+5Byozs"
        "/egrm3d8wm2grAlrg/LfTd0l6E8IWnAb8t+Nl6p3wh"
        "/krXoeRxJgmQ4CYsIxnTAj6AK97U3wO51sWrp7hSAIaS58XWXw0ELpzZa/oIsMoIgP"
        "+hxnp9sNU9H7DA== "
    )
    print(f"Decrypted string: {plain_text}")
