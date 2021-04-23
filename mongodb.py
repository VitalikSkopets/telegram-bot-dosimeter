from datetime import datetime
import pytz
import locale
from pymongo import MongoClient
from config import MONGODB_REF, MONGO_DB, TOKEN_FOR_ENCRYPT_DB
from utilities import encryption
from loguru import logger

mdb = MongoClient(MONGODB_REF)[MONGO_DB]

tz_minsk = pytz.timezone('Europe/Minsk')
today = datetime.now(tz_minsk).strftime("%a %d-%b-%Y %H:%M:%S")
locale.setlocale(category=locale.LC_ALL, locale="Russian")


def create_collection(user):
    """
    Функция создает объект с типом данных "словарь", содержащий в качестве ключей "идентификационные данные
    пользователя" и доступный перечень "действий" бота. Значения ключей first_name, last_name и username добавляются
    в словарь в зашифрованном виде с использованием кастомной функции encryption(), а значениями "действий" бота
    являются пустые массивы (списки), в которые впоследствии будут добавлятся дата и время их совершения
    :param user: словарь update.effective_user с идентификационными данными пользователя Telegram
    :return: словарь current_user, являющийся документов для добавления в коллекцию users БД users_db в MongoDB Atlas
    """
    current_user = {'user_id': user['id'],
                    'first_name': encryption(TOKEN_FOR_ENCRYPT_DB, user['first_name']),
                    'last_name': encryption(TOKEN_FOR_ENCRYPT_DB, user['last_name']),
                    'user_name': encryption(TOKEN_FOR_ENCRYPT_DB, user['username']),
                    'selected /start command': [],
                    'selected /help command': [],
                    'sent a welcome text message': [],
                    'press button "Radioactive monitoring"': [],
                    'press button "Observation points"': [],
                    'press button "Send geolocation"': []
                    }
    return current_user


def add_db_start(mdb, user):
    """
    Функция добавляет текущую дату и время вызова команды /start пользователя Telegram в массив с ключом
    "selected /start command" коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        mdb.users.insert_one(create_collection(user))
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'selected /start command': today}})
        logger.info('User added in db after select /start command')
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'selected /start command': today}})
        logger.info('In db updated date and time user select /start command')


def add_db_help(mdb, user):
    """
    Функция добавляет текущую дату и время вызова команды /help пользователя Telegram в массив с ключом
    "selected /help command" коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        mdb.users.insert_one(create_collection(user))
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'selected /help command': today}})
        logger.info('User added in db after select /help command')
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'selected /help command': today}})
        logger.info('In db updated date and time user select /help command')


def add_db_messages(mdb, user):
    """
    Функция добавляет текущую дату и время отправки пользователем приветственного сообщения в массив с ключом
    "sent a welcome text message" коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных MongoDB
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    if mdb.users.find_one({'user_id': user['id']}) is None:
        mdb.users.insert_one(create_collection(user))
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'sent a welcome text message': today}})
        logger.info('User added in db after send a welcome text message')
    elif mdb.users.find_one({'user_id': user['id']}) is not None:
        mdb.users.update_one({'user_id': user['id']},
                             {'$push': {'sent a welcome text message': today}})
        logger.info('In db updated date and time user send a welcome text message')


def add_db_radioactive_monitoring(mdb, user):
    """
    Функция добавляет текущую дату и время при нажатии пользователем кнопки "Радиационный мониторирг"в массив с ключом
    "press button 'Radioactive monitoring'" соответствующего документа коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$push': {'press button "Radioactive monitoring"': today}})
    logger.info('In db added date and time user press button "Radioactive monitoring"')


def add_db_scraper(mdb, user):
    """
    Функция добавляет текущую дату и время при нажатии пользователем кнопки "Пункты наблюдения" в массив с ключом
    "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$push': {'press button "Observation points"': today}})
    logger.info('In db added date and time user press button "Observation points"')


def add_db_geolocation(mdb, user):
    """
    Функция добавляет текущую дату и время при нажатии пользователем кнопки "Отправить мою геолокацию" в массив
    с ключом "press button 'Send geolocation'" соответствующего документа коллекции users users_db в MongoDB Atlas
    :param mdb: инстанцированный объект класса MongoClient из модуля pymongo - соединение с базай данных
    :param user: словарь update.effective_user с информацией о пользователе Telegram
    :return: None
    """
    mdb.users.update_one({'user_id': user['id']},
                         {'$push': {'press button "Send geolocation"': today}})
    logger.info('In db added date and time user press button "Send geolocation"')
