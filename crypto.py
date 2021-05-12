import os
import rsa
from loguru import logger
from typing import Optional


class Crypt:

    @staticmethod
    def __gen_cryptokeys() -> None:
        """
        Функция генерирует пару ключей (публичный и приватный) и записывает их в файлы pubkey.pem и private.pem,
        соответственно, для дальнейшего шифрования/дешифрования стркоовых объектов алгоритмом ассиметричного RSA
        шифрования

        :return: None
        """
        try:
            (pubkey, privkey) = rsa.newkeys(512, accurate=False)
            pubkey_pem = pubkey.save_pkcs1()
            privkey_pem = privkey.save_pkcs1()
            with open('private.pem', mode='wb') as privatefile, open(r'public.pem', mode='wb') as publicfile:
                privatefile.write(privkey_pem)
                publicfile.write(pubkey_pem)
        except FileExistsError:
            logger.exception('Files with extensions *.pem in the predefined directory already exist', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the _gen_cryptokeys() function', traceback=True)

    @staticmethod
    def __get_pubkey() -> rsa.PublicKey:
        """
        Функция открывает для чтения файл public.pem и возвращает, записанный в нем публичный ключ для шифрования
        строкового объекта

        :return: pubkey - публичный ключ шифрования
        """
        try:
            while os.path.exists('public.pem') is False:
                Crypt.__gen_cryptokeys()
                continue
            else:
                with open('public.pem', mode='rb') as pubfile:
                    pubkeydata = pubfile.read()
                    pubkey = rsa.PublicKey.load_pkcs1(pubkeydata)
                    return pubkey
        except FileNotFoundError:
            logger.exception('File public.pem not found!', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the __get_pubkey() function', traceback=True)

    @staticmethod
    def __get_privkey() -> rsa.PrivateKey:
        """
        Функция открывает для чтения файл private.pem и возвращает, записанный в нем приватный(закрытый) ключ для
        дешифрования байтовой строки - полседолвательности байт

        :return: privkey - приватный (закрытый) ключ для дешифрования
        """
        try:
            while os.path.exists('private.pem') is False:
                Crypt.__gen_cryptokeys()
                continue
            else:
                with open('private.pem', mode='rb') as privfile:
                    privkeydata = privfile.read()
                    privkey = rsa.PrivateKey.load_pkcs1(privkeydata)
                    return privkey
        except FileNotFoundError:
            logger.exception('File private.pem not found!', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the __get_privkey() function', traceback=True)

    def __init__(self, line: str, pubkey=__get_pubkey, privkey=__get_privkey) -> None:
        """
        Конструктор инициализации объектов класса Crypt

        :param line: строковый объект - идентификацуионные данные пользователя - значения ключей first_name, last_name,
        username из словаря update.effective_user

        :param pubkey: публичный ключ шифрования

        :param privkey: приватный ключ дешифрвоания
        """
        self.line = line
        self.pubkey = pubkey
        self.privkey = privkey

    @staticmethod
    def encrypt(line: str, pubkey=__get_pubkey) -> Optional[list[int]]:
        """
        Функция ассиметричного RSA шифрования строковых объектов - идентификацуионных данных пользователей. Данные
        шифруются с использованием публичного ключа, который читается из файла public.pem, после чего преобразуются
        в массив целых чисел для последующего долговременного хранениния в коллекции users базы данных MongoDB Atlas
        в полях с ключами first_name, last_name и username

        :param line: строковый объект - идентификацуионные данные пользователя - значения ключей first_name, last_name,
        username из словаря update.effective_user

        :param pubkey: публичный ключ шифрования

        :return token_lst: шифрованный стрковый объект в байтовом представлении преобразованный в массив целых чисел
        для последующего помещения в коллекцию users базы данных MongoDB Atlas в полях с ключами first_name, last_name
        и username
        """
        try:
            if isinstance(line, str):
                token = rsa.encrypt(line.encode(), Crypt.__get_pubkey())
                token_lst = list(token)
                return token_lst
            elif not line:
                return None
        except Exception:
            logger.exception('ERROR while performing the encrypt() function', traceback=True)

    @staticmethod
    def decrypt(token_lst: list[int], privkey=__get_privkey) -> str:
        """
        Функция дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся в коллекции users
        базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные преобразуются из массива
        целых чисел в байтовую строку, после чего дешифруются с использованием приватного (закрытого) ключа, который
        читается из файла privat.pem

        :param token_lst: строковый объект - идентификацуионные данные пользователя - значения ключей first_name,
        last_name, username из словаря update.effective_user

        :param privkey: приватный (закрытый) ключ дешифрования

        :return line: дешифрованный стрковый объект - - идентификацуионные данные пользователя из коллекции users базы
        данных MongoDB Atlas в полях с ключами first_name, last_name и username
        """
        try:
            if isinstance(token_lst, list):
                line = rsa.decrypt(bytes(token_lst), Crypt.__get_privkey())
                return line.decode()
        except Exception:
            logger.exception('ERROR while performing the encrypt() function', traceback=True)


class Decryptor:

    def __init__(self, token) -> None:
        """
        Конструктор инициализации объектов класса Decryptor

        :param token: шифрованный стрковый объект в байтовом представлении, хранящийся в коллекции users базы данных
        MongoDB Atlas в полях с ключами first_name, last_name и(или) username
        """
        self.token = token

    def decrypt(self) -> str:
        """
        Функция дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся в коллекции users
        базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные дешифруются с
        использованием приватного (закрытого) ключа, который читается из файла privat.pem

        :return line: дешифрованный стрковый объект - - идентификацуионные данные пользователя из коллекции users базы
        данных MongoDB Atlas в полях с ключами first_name, last_name и username
        """
        with open('private.pem', mode='rb') as privfile:
            privkeydata = privfile.read()
            privkey = rsa.PrivateKey.load_pkcs1(privkeydata)
        line = rsa.decrypt(self.token, privkey)
        return line.decode()


if __name__ == '__main__':
    a = Crypt('Rrrrr')
    print(a.encrypt('Rrrrr'))
    print(a.decrypt([13, 179, 191, 91, 23, 237, 226, 52, 157, 77, 108, 8, 179, 80, 188, 91, 158, 118, 127, 179, 153,
                     187, 131, 36, 223, 107, 199, 238, 75, 157, 217, 39, 109, 4, 64, 92, 47, 83, 118, 96, 99, 191,
                     99, 238, 174, 124, 33, 211, 39, 121, 106, 110, 253, 189, 165, 173, 147, 93, 84, 36, 117, 75,
                     221, 3
                     ]
                    )
          )
    print()
    b = Decryptor(
        b'Q\x88\x1fr8-\xf0<\x18\xde\x068\x93\xa9\xaaT\xa4\xf9%L\xdcV\xd6\xcb\x83\xd9\x01\x00\x9b\xee\x1c\x11J/\xef'
        b'\xabT\x00\xbf\xee\x06\xa5\xcd\x84A\x0e \x8cf)\xcd\xcd5\x1d\xd3\xb6\xebS\xe0\xcd\xd76\xf4\xb5')
    print(b.decrypt())
