import base64
import os
from typing import NoReturn

import rsa

__all__ = ("DataEncrypt",)


class DataEncrypt:
    def __init__(self, line: str, token: str | bytes | None = None) -> None:
        """
        Конструктор инициализации объектов класса DataEncrypt. В ходе выполнения
        проверяет наличие в заданной дериктории файлов 'private.pem' и 'public.pem' с
        записанными в них публичным и приватным ключами шифрования/дешифрования,
        и в случае их отсутствия генерирует и записывает в файлы связку из публичного
        и приватного ключей необходимых для ассиметричного RSA шифрования строковых
        объектов
        :param line: строковый объект -> идентификацуионные данные пользователя -
        значения ключей first_name, last_name, username
        :param token: зашифрованный строковый объект - идентификацуионные данные
        пользователя - значения ключей first_name, last_name, username
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

    def encrypt(self) -> str | NoReturn:
        """
        Функция ассиметричного RSA шифрования строковых объектов - идентификацуионных
        данных пользователей. Данные шифруются с использованием публичного ключа,
        который читается из файла public.pem, после чего преобразуются в строковый
        объект в кодировке base64 для последующего долговременного хранениния в
        коллекции users базы данных MongoDB Atlas в полях с ключами first_name,
        last_name и username
        :return строковый объект в кодировке base64
        """
        if isinstance(self.line, str):
            with open("../public.pem", mode="rb") as pubfile:
                pubkeydata = pubfile.read()
                pub_key = rsa.PublicKey.load_pkcs1(pubkeydata)
            pre_token = rsa.encrypt(self.line.encode(), pub_key)  # type: ignore
            self.token = base64.b64encode(pre_token)
            return self.token.decode("UTF-8")
        return

    def decrypt(self) -> str:
        """
        Функция дешифрования строковых объектов - идентификацуионных данных
        пользователей, хранящихся в коллекции users базы данных MongoDB Atlas в полях
        с ключами first_name, last_name и username. Данные дешифруются с использованием
        приватного (закрытого) ключа, который читается из файла privat.pem
        :return line: дешифрованный стрковый объект - - идентификацуионные данные
        пользователя из коллекции users базы данных MongoDB Atlas в полях с ключами
        first_name, last_name и username
        """
        with open("../private.pem", mode="rb") as privfile:
            privkeydata = privfile.read()
            priv_key = rsa.PrivateKey.load_pkcs1(privkeydata)
        token = base64.b64decode(self.token)  # type: ignore
        line = rsa.decrypt(token, priv_key)  # type: ignore
        return line.decode()


if __name__ == "__main__":
    a = DataEncrypt("Test string")
    ciphertext = a.encrypt()
    print(ciphertext)
    print(a.decrypt())
