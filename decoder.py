from config import SECRET_KEY


def decrypt(token, key=SECRET_KEY):
    """
    Функция дешифрования строковых объектов - идентификацуионных данных пользователей, хранящихся
    в коллекции users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
    :param key: сгенерированный ключ шифрования/дешифрования
    :param token: строковый объект - шифрованый текст полей с ключами first_name и(или)
    last_name, username коллекции users базы данных MongoDB Atlas
    :return: строковый объект - дешифрованный текст полей с ключами  first_name и(или) last_name,
    username коллекции users базы данных MongoDB Atlas
    """
    line = key.decrypt(token.encode())
    return line.decode()


if __name__ == "__main__":
    print(decrypt('gAAAAABgioYkOIrn__YvhD1awR3DLpabyM6UaZVlXxxFfjAU6G-035u7m0b3pwEwNAE4aqk8w40OmiiIDzvmBYBLAdz5IE3LpQ=='))
