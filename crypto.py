import rsa
from loguru import logger

def crypto() -> None:
    """
    Функция генерирует пару ключей (публичный и приватный) и записывает их в файлы pubkey.pem и private.pem,
    соответственно для дальнейшего ассиметричного RSA шифрования/дешифрования стркоовых объектов
    :return: None
    """
    try:
        (pubkey, privkey) = rsa.newkeys(512, accurate=False)
        pubkey_pem = pubkey.save_pkcs1()
        privkey_pem = privkey.save_pkcs1()
        with open('private.pem', mode='wb') as privatefile, open(r'public.pem', mode='wb') as publicfile:
            privatefile.write(privkey_pem)
            publicfile.write(pubkey_pem)
        return None
    except Exception:
        logger.exception('ERROR while performing the crypto() function', traceback=True)


def decoder(token: bytes) -> str:
    """
    Функия дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся в коллекции users
    базы данных MongoDB Atlas в полях с ключами first_name, last_name и username. Данные дешифруются
    с использованием приватного ключа, который читается из файла private.pem
    :param token: байтовые строки - последовательность байт - зашифрованные идентификацуионные данные пользователей,
    хранящиеся в коллекции users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
    :return: строковый объект - дешифрованные идентификацуионные данные пользователей, хранящиеся в коллекции users
    базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
    """
    try:
        with open('private.pem', mode='rb') as privatefile:
            keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        line = rsa.decrypt(token, privkey)
        return line.decode('utf8')
    except FileNotFoundError:
        logger.exception('File private.pem not found!', traceback=True)
    except Exception:
        logger.exception('ERROR while performing the decoder() function', traceback=True)


if __name__ == '__main__':
    # crypto()
    print(decoder(b''))
