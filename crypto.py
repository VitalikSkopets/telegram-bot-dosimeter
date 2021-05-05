import os
import rsa
from loguru import logger


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
    def __get_pubkey():
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
    def __get_privkey():
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

    def __init__(self, line: str, pubkey=__get_pubkey, privkey=__get_privkey):
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

    def encrypt(line: str, pubkey=__get_pubkey) -> str:
        """
        Функция ассиметричного RSA шифрования строковых объектов - идентификацуионных данных пользователей, хранящихся
        в коллекции users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные шифруются
        с использованием публичного ключа, который читается из файла public.pem

        :param line: строковый объект - идентификацуионные данные пользователя - значения ключей first_name, last_name,
        username из словаря update.effective_user

        :param pubkey: публичный ключ шифрования

        :return token_str: шифрованный стрковый объект в байтовом представлении преобразованный в строку для помещения в
        коллекцию users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
        """
        try:
            if line is not None:
                token = rsa.encrypt(line.encode(), pubkey())
                token_str = str(token)
                return token_str
        except Exception:
            logger.exception('ERROR while performing the encrypt() function', traceback=True)

    def decrypt(self, token: bytes = encrypt, privkey=__get_privkey) -> str:
        """
        Функия дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся в коллекции users
        базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные дешифруются
        с использованием приватного ключа, который читается из файла private.pem

        :param privkey: приватный ключ дешифрования

        :param token: байтовая строка - последовательность байт - зашифрованные идентификацуионные данные пользователей,
        хранящиеся в коллекции users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username

        :return: строковый объект - дешифрованные идентификацуионные данные пользователей, хранящиеся в коллекции users
        базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
        """
        try:
            line = rsa.decrypt(token(self, pubkey=Crypt.__get_pubkey), privkey())
            return line.decode()
        except Exception:
            logger.exception('ERROR while performing the decrypt() function', traceback=True)


if __name__ == '__main__':
    a = Crypt("Rrrrrrrrrrrrrrrrr")
    print(a.line)
    print(a.encrypt())
    print(a.decrypt())
