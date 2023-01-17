import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import rsa

from dosimeter.config import BASE_DIR

__all__ = ("DataEncrypt", "cryptographer")


@dataclass(frozen=True)
class Files:
    SECRET_KEY: Path = BASE_DIR / "private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "public.pem"


class DataEncrypt:
    def __init__(
        self,
        sec_key_path: Path = Files.SECRET_KEY,
        pub_key_path: Path = Files.PUBLIC_KEY,
    ) -> None:
        """
        Constructor for initializing objects of the DataEncrypt class. In the course
        of execution, it checks for the presence in the specified directory of the
        private.pem and public.pem files with the public and private
        encryption/decryption keys stored in them, and if they are absent,
        it generates and writes to the files a bunch of public and private keys
        necessary for asymmetric RSA encryption of string objects.
        """
        self.sec_key_path = sec_key_path
        self.pub_key_path = pub_key_path

        if os.path.exists(self.sec_key_path and self.pub_key_path):
            return
        (pubkey, privkey) = rsa.newkeys(512, accurate=False)
        pubkey_pem = pubkey.save_pkcs1()
        privkey_pem = privkey.save_pkcs1()
        with open(self.sec_key_path, mode="wb") as privatefile, open(
            self.pub_key_path, mode="wb"
        ) as publicfile:
            privatefile.write(privkey_pem)
            publicfile.write(pubkey_pem)

    def encrypt(self, line: str | None = None) -> str | None:
        """
        The function of asymmetric RSA encryption of string objects - user
        identification data. The data is encrypted using the public key, which is
        read from the public.pem file, and then converted into a base64 encoded
        string object for subsequent long-term storage in the users collection of the
        MongoDB Atlas database in the fields with the keys first_name, last_name and
        username.
        """
        if not isinstance(line, str):
            return None
        with open(self.pub_key_path, mode="rb") as pubfile:
            pubkeydata = pubfile.read()
            pub_key = rsa.PublicKey.load_pkcs1(pubkeydata)
        pre_token = rsa.encrypt(line.encode(), pub_key)
        token = base64.b64encode(pre_token)
        return token.decode("UTF-8")

    def decrypt(self, token: Any) -> str | None:
        """
        A function for decrypting string objects - user identification data stored in
        the users collection of the MongoDB Atlas database in fields with the keys
        first_name, last_name and username. The data is decrypted using a private (
        private) key, which is read from the privat.pem file.
        """
        if not token:
            return None
        with open(self.sec_key_path, mode="rb") as privfile:
            privkeydata = privfile.read()
            priv_key = rsa.PrivateKey.load_pkcs1(privkeydata)
        pre_token = base64.b64decode(token)
        line = rsa.decrypt(pre_token, priv_key)
        return line.decode()


"""DataEncrypt class instance"""
cryptographer = DataEncrypt()

if __name__ == "__main__":
    ciphertext = cryptographer.encrypt("Test string")
    enc_text = cryptographer.decrypt(
        token="H32DeNHeTB2rb6m5WyRUsaT5qCN9Cj1D5LEQJ4D/EEJYBDRH+uraSb2JpwTwBmdr"
        "/anTnSlnMa3+iD2wwLi6Cw== "
    )
    print(f"Encrypted string: {ciphertext}")
    print(f"Decrypted string: {enc_text}")
