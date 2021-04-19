import datetime
from pymongo import MongoClient

from config import MONGODB_REF, MONGO_DB

mdb = MongoClient(MONGODB_REF)[MONGO_DB]
today = datetime.datetime.today().strftime("%a %d-%b-%Y %H:%M:%S")


def add_db_send_welcome(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию users базы данных MongoDB при вызове команды /start
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:

        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': message_inf['message']['chat']['first_name'],
                'last_name': message_inf['message']['chat']['last_name'],
                'user_name': message_inf['message']['chat']['username'],
                'selected /start command': today
                }
        mdb.users.insert_one(user)
    elif mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is not None:
        mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                             {'$set': {'selected /start command': today}})


def add_db_send_help(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию users базы данных MongoDB при вызове команды /help
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:
        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': message_inf['message']['chat']['first_name'],
                'last_name': message_inf['message']['chat']['last_name'],
                'user_name': message_inf['message']['chat']['username'],
                'selected /help command': today
                }
        mdb.users.insert_one(user)
    elif mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is not None:
        mdb.users.update_one({'user_id': message_inf['message']['chat']['id']},
                             {'$set': {'selected /help command': today}})


def add_db_get_text_messages(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию users базы данных MongoDB при отправке пользователем боту
    приветственного сообщения
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    if mdb.users.find_one({'user_id': message_inf['message']['chat']['id']}) is None:
        user = {'user_id': message_inf['message']['chat']['id'],
                'first_name': message_inf['message']['chat']['first_name'],
                'last_name': message_inf['message']['chat']['last_name'],
                'user_name': message_inf['message']['chat']['username'],
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
