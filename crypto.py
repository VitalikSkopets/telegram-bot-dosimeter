import os
import rsa
from typing import Optional


class Crypt:

    def __init__(self, line: str) -> None:
        """
        Конструктор инициализации объектов класса Crypt, генерации и записи в файлы публичного и приватного ключей для
        ассиметричного RSA шифрования строковых объектов

        :param line: строковый объект -> идентификацуионные данные пользователя - значения ключей first_name, last_name,
        username из словаря update.effective_user -> подлежэащий шифрованию
        """
        self.line = line
        (pubkey, privkey) = rsa.newkeys(512, accurate=False)
        pubkey_pem = pubkey.save_pkcs1()
        privkey_pem = privkey.save_pkcs1()
        with open('private.pem', mode='wb') as privatefile, open('public.pem', mode='wb') as publicfile:
            privatefile.write(privkey_pem)
            publicfile.write(pubkey_pem)

    @staticmethod
    def encrypt(line: str) -> Optional[list[int]]:
        """
        Функция ассиметричного RSA шифрования строковых объектов - идентификацуионных данных пользователей. Данные
        шифруются с использованием публичного ключа, который читается из файла public.pem, после чего преобразуются
        в массив целых чисел для последующего долговременного хранениния в коллекции users базы данных MongoDB Atlas
        в полях с ключами first_name, last_name и username

        :param line: строковый объект -> идентификацуионные данные пользователя - значения ключей first_name, last_name,
        username из словаря update.effective_user -> подлежэащий шифрованию

        :return шифрованный стрковый объект в байтовом представлении, дополнительно преобразованный в массив целых
        чисел для последующего помещения в коллекцию users базы данных MongoDB Atlas в полях с ключами first_name,
        last_name и username
        """
        if os.path.exists('private.pem' and 'public.pem'):
            with open('public.pem', mode='rb') as pubfile:
                pubkeydata = pubfile.read()
                pubkey = rsa.PublicKey.load_pkcs1(pubkeydata)
            return list(rsa.encrypt(line.encode(), pubkey))
        Crypt.__init__(line)

    @staticmethod
    def decrypt(token: list[int]) -> str:
        """
        Функция дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся в коллекции users
        базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные преобразуются из массива
        целых чисел в байтовую строку, после чего дешифруются с использованием приватного (закрытого) ключа, который
        читается из файла privat.pem

        :param token: массив целых чисел - зашифрованный строковый объект - идентификацуионные данные пользователя -
        значения ключей first_name, last_name, username из словаря update.effective_user

        :return line: дешифрованный стрковый объект - - идентификацуионные данные пользователя из коллекции users базы
        данных MongoDB Atlas в полях с ключами first_name, last_name и username
        """
        with open('private.pem', mode='rb') as privfile:
            privkeydata = privfile.read()
            privkey = rsa.PrivateKey.load_pkcs1(privkeydata)
        line = rsa.decrypt(bytes(token), privkey)
        return line.decode()


if __name__ == '__main__':
    a = Crypt('Test string')
    ciphertext = a.encrypt('Test string')
    print(ciphertext)
    print(a.decrypt(ciphertext))
