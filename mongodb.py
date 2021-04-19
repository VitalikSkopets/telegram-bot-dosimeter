import datetime
from pymongo import MongoClient

from config import MONGODB_REF, MONGO_DB

mdb = MongoClient(MONGODB_REF)[MONGO_DB]
today = datetime.datetime.today().strftime("%a %d-%b-%Y %H:%M:%S")
actions = ['Selected /start command',
           'selected /help command',
           'Sent a welcome text message',
           'Press button "Radioactive monitoring"',
           'Press button "Observation points"',
           'Press button "Send geolocation"'
           ]

def add_db_send_welcome(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию send_welcom базы данных MongoDB при вызове команды /start
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[0],
            'date': today
            }
    mdb.users.insert_one(user)


def add_db_send_help(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию send_help базы данных MongoDB при вызове команды /help
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[1],
            'date': today
            }
    mdb.users.insert_one(user)


def add_db_get_text_messages(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию get_text_messages базы данных MongoDB при отправке пользователем боту
    приветственного сообщения
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[2],
            'date': today
            }
    mdb.users.insert_one(user)


def add_db_radioactive_monitoring(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию radioactive_monitoring базы данных MongoDB при нажатии пользователем
    кнопки "Радиационный мониторирг"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[3],
            'date': today
            }
    mdb.users.insert_one(user)


def add_db_scraper(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию scraper базы данных MongoDB при нажатии пользователем кнопки
    "Пункты наблюдения"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[4],
            'date': today
            }
    mdb.users.insert_one(user)


def add_db_geolocation(mdb, message_inf):
    '''
    Функция добавляет пользователя в коллекцию scraper базы данных MongoDB при нажатии пользователем кнопки
    "Отправить мою геолокацию"
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param message_inf: словарь update с информацией о пользователе Telegram
    :return: None
    '''
    user = {'user_id': message_inf['message']['chat']['id'],
            'first_name': message_inf['message']['chat']['first_name'],
            'last_name': message_inf['message']['chat']['last_name'],
            'user_name': message_inf['message']['chat']['username'],
            'action': actions[5],
            'date': today
            }
    mdb.users.insert_one(user)
