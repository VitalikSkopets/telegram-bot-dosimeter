import datetime
from pymongo import MongoClient
from config import MONGODB_REF, MONGO_DB, TOKEN_FOR_DB
from utilities import encryption

mdb = MongoClient(MONGODB_REF)[MONGO_DB]
today = datetime.datetime.today().strftime("%a %d-%b-%Y %H:%M:%S")


def add_db_send_welcome(mdb, message_inf):
    '''
    Функция добавляет chat_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при вызове пользователем команды /start
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    firstname = message_inf['message']['chat']['first_name']
    lastname = message_inf['message']['chat']['last_name']
    username = message_inf['message']['chat']['username']

    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_DB, firstname)
        encrypted_lastname = encryption(TOKEN_FOR_DB, lastname)
        encrypted_username = encryption(TOKEN_FOR_DB, username)

        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': encrypted_firstname,
                'last_name': encrypted_lastname,
                'user_name': encrypted_username,
                'selected /start command': today
                }
        mdb.users.insert_one(user)
    elif mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is not None:
        mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                             {'$set': {'selected /start command': today}})


def add_db_send_help(mdb, message_inf):
    '''
    Функция добавляет chat_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при вызове пользователем команды /help
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    firstname = message_inf['message']['chat']['first_name']
    lastname = message_inf['message']['chat']['last_name']
    username = message_inf['message']['chat']['username']

    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_DB, firstname)
        encrypted_lastname = encryption(TOKEN_FOR_DB, lastname)
        encrypted_username = encryption(TOKEN_FOR_DB, username)

        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': encrypted_firstname,
                'last_name': encrypted_lastname,
                'user_name': encrypted_username,
                'selected /help command': today
                }
        mdb.users.insert_one(user)
    elif mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is not None:
        mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                             {'$set': {'selected /help command': today}})


def add_db_get_text_messages(mdb, message_inf):
    '''
    Функция добавляет chat_id пользователя, а также в шифрованные данные: first_name, last_name и username,
    в коллекцию users базы данных MongoDB при отправке пользователем боту приветственного сообщения
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    firstname = message_inf['message']['chat']['first_name']
    lastname = message_inf['message']['chat']['last_name']
    username = message_inf['message']['chat']['username']

    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:
        encrypted_firstname = encryption(TOKEN_FOR_DB, firstname)
        encrypted_lastname = encryption(TOKEN_FOR_DB, lastname)
        encrypted_username = encryption(TOKEN_FOR_DB, username)

        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': encrypted_firstname,
                'last_name': encrypted_lastname,
                'user_name': encrypted_username,
                'sent a welcome text message': today
                }
        mdb.users.insert_one(user)
    elif mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is not None:
        mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                             {'$set': {'sent a welcome text message': today}})


def add_db_radioactive_monitoring(mdb, message_inf):
    '''
    Функция добавляет ключ 'press button "Radioactive monitoring"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Радиационный мониторирг"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                         {'$set': {'press button "Radioactive monitoring"': today}})


def add_db_scraper(mdb, message_inf):
    '''
    Функция добавляет ключ 'press button "Observation points"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Пункты наблюдения"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                         {'$set': {'press button "Observation points"': today}})


def add_db_geolocation(mdb, message_inf):
    '''
    Функция добавляет ключ 'press button "Send geolocation"' в коллекцию users базы данных MongoDB
    при нажатии пользователем кнопки "Отправить мою геолокацию"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                         {'$set': {'press button "Send geolocation"': today}})
