from datetime import datetime
import pytz
from pymongo import MongoClient
from config import MONGODB_REF, MONGO_DB, TOKEN_FOR_ENCRYPT_DB
from utilities import encryption

mdb = MongoClient(MONGODB_REF)[MONGO_DB]

tz_minsk = pytz.timezone('Europe/Minsk')
today = datetime.now(tz_minsk).strftime("%a %d-%b-%Y %H:%M:%S")


def add_db_start(mdb, user):
    """
    Функция добавляет user_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при вызове пользователем команды /start
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_ENCRYPT_DB, user['first_name'])
        encrypted_lastname = encryption(TOKEN_FOR_ENCRYPT_DB, user['last_name'])
        encrypted_username = encryption(TOKEN_FOR_ENCRYPT_DB, user['username'])

        current_user = {'user_id': user['id'],
                        'first_name': encrypted_firstname,
                        'last_name': encrypted_lastname,
                        'user_name': encrypted_username,
                        'selected /start command': today
                        }
        mdb.users.insert_one(current_user)
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$set': {'selected /start command': today}})


def add_db_help(mdb, user):
    """
    Функция добавляет user_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при вызове пользователем команды /help
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_ENCRYPT_DB, user['first_name'])
        encrypted_lastname = encryption(TOKEN_FOR_ENCRYPT_DB, user['last_name'])
        encrypted_username = encryption(TOKEN_FOR_ENCRYPT_DB, user['username'])

        current_user = {'user_id': user['id'],
                        'first_name': encrypted_firstname,
                        'last_name': encrypted_lastname,
                        'user_name': encrypted_username,
                        'selected /help command': today
                        }
        mdb.users.insert_one(current_user)
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$set': {'selected /help command': today}})


def add_db_messages(mdb, user):
    """
    Функция добавляет user_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при отправке пользователем боту приветственного сообщения
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_ENCRYPT_DB, user['first_name'])
        encrypted_lastname = encryption(TOKEN_FOR_ENCRYPT_DB, user['last_name'])
        encrypted_username = encryption(TOKEN_FOR_ENCRYPT_DB, user['username'])

        current_user = {'user_id': user['id'],
                        'first_name': encrypted_firstname,
                        'last_name': encrypted_lastname,
                        'user_name': encrypted_username,
                        'sent a welcome text message': today
                        }
        mdb.users.insert_one(current_user)
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$set': {'sent a welcome text message': today}})


def add_db_radioactive_monitoring(mdb, user):
    """
    Функция добавляет ключ 'press button "Radioactive monitoring"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Радиационный мониторирг"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$set': {'press button "Radioactive monitoring"': today}})


def add_db_scraper(mdb, user):
    """
    Функция добавляет ключ 'press button "Observation points"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Пункты наблюдения"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$set': {'press button "Observation points"': today}})


def add_db_geolocation(mdb, user):
    """
    Функция добавляет ключ 'press button "Send geolocation"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Отправить мою геолокацию"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: update.effective_user - словарь с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$set': {'press button "Send geolocation"': today}})
