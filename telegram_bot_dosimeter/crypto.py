import base64
import os

import rsa

__all__ = ("DataEncrypt",)


class DataEncrypt:
    def __init__(
        self, line: str | None = None, *, token: str | bytes | None = None
    ) -> None:
        """
        Constructor for initializing objects of the DataEncrypt class. In the course
        of execution, it checks for the presence in the specified directory of the
        private.pem and public.pem files with the public and private
        encryption/decryption keys stored in them, and if they are absent,
        it generates and writes to the files a bunch of public and private keys
        necessary for asymmetric RSA encryption of string objects.
        """
        self.line = line
        self.token = token
        if os.path.exists("../private.pem" and "../public.pem"):
            return
        (pubkey, privkey) = rsa.newkeys(512, accurate=False)
        pubkey_pem = pubkey.save_pkcs1()
        privkey_pem = privkey.save_pkcs1()
        with open("../private.pem", mode="wb") as privatefile, open(
            "../public.pem", mode="wb"
        ) as publicfile:
            privatefile.write(privkey_pem)
            publicfile.write(pubkey_pem)

    def encrypt(self) -> str | None:
        """
        The function of asymmetric RSA encryption of string objects - user
        identification data. The data is encrypted using the public key, which is
        read from the public.pem file, and then converted into a base64 encoded
        string object for subsequent long-term storage in the users collection of the
        MongoDB Atlas database in the fields with the keys first_name, last_name and
        username.
        """
        if isinstance(self.line, str):
            with open("../public.pem", mode="rb") as pubfile:
                pubkeydata = pubfile.read()
                pub_key = rsa.PublicKey.load_pkcs1(pubkeydata)
            pre_token = rsa.encrypt(self.line.encode(), pub_key)  # type: ignore
            self.token = base64.b64encode(pre_token)
            return self.token.decode("UTF-8")
        return None

    def decrypt(self) -> str:
        """
        A function for decrypting string objects - user identification data stored in
        the users collection of the MongoDB Atlas database in fields with the keys
        first_name, last_name and username. The data is decrypted using a private (
        private) key, which is read from the privat.pem file.
        """
        with open("../private.pem", mode="rb") as privfile:
            privkeydata = privfile.read()
            priv_key = rsa.PrivateKey.load_pkcs1(privkeydata)
        token = base64.b64decode(self.token)  # type: ignore
        line = rsa.decrypt(token, priv_key)  # type: ignore
        return line.decode()


if __name__ == "__main__":
    text = DataEncrypt("Test string")
    ciphertext = text.encrypt()
    print(f"Encrypted string: {ciphertext}")
    print(f"Decrypted string: {text.decrypt()}")
    enc_text = DataEncrypt(
        token="H32DeNHeTB2rb6m5WyRUsaT5qCN9Cj1D5LEQJ4D/EEJYBDRH"
        "+uraSb2JpwTwBmdr/anTnSlnMa3+iD2wwLi6Cw=="
    )
    print(f"Decrypted string: {enc_text.decrypt()}")
