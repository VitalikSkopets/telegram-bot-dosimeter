from datetime import datetime
from typing import Final, Any
import pytz
import locale
from pymongo import MongoClient
from config import MONGODB_REF, MONGO_DB
from crypto import Crypt
from loguru import logger

locale.setlocale(category=locale.LC_ALL, locale="Russian")
tz_minsk: Final = pytz.timezone('Europe/Minsk')
today: Final = datetime.now(tz_minsk).strftime("%a %d-%b-%Y %H:%M:%S")
mdb: Final = MongoClient(MONGODB_REF)[MONGO_DB]


class DB:

    def __init__(self, mdb):
        """
        Конструктор инициализации объектов класса DB

        :param mdb: соединение с базой данных users_db в MongoDB Atlas
        """
        self.mdb = mdb

    @staticmethod
    def create_collection(user: dict[str, any]) -> dict[str, any]:
        """
        Функция создает объект с типом данных "словарь", содержащий в качестве ключей "идентификационные данные
        пользователя" и доступный перечень "действий" бота. Значения ключей first_name, last_name и username добавляются
        в словарь в зашифрованном виде с использованием метода encrypt() из класса Crypt, а значениями "действий" бота
        являются пустые массивы (списки), в которые впоследствии будут добавлятся дата и время их совершения

        :param user: словарь update.effective_user с идентификационными данными пользователя Telegram

        :return: словарь current_user, являющийся документов для добавления в коллекцию users БД users_db в MongoDB
        """
        current_user = {'user_id': user['id'],
                        'first_name': Crypt.encrypt(user['first_name']),
                        'last_name': Crypt.encrypt(user['last_name']),
                        'user_name': Crypt.encrypt(user['username']),
                        'selected /start command': [],
                        'selected /help command': [],
                        'sent a welcome text message': [],
                        'press button "Radioactive monitoring"': [],
                        'press button "Observation points"': [],
                        'press button "Brest region"': [],
                        'press button "Vitebsk region"': [],
                        'press button "Gomel region"': [],
                        'press button "Grodno region"': [],
                        'press button "Minsk region"': [],
                        'press button "Mogilev region"': [],
                        'press button "Send geolocation"': []
                        }
        return current_user

    @staticmethod
    def add_db_start(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время вызова команды /start пользователя Telegram в массив с ключом
        "selected /start command" коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            if mdb.users.find_one({'user_id': user['id']}) is None:
                mdb.users.insert_one(DB.create_collection(user))
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'selected /start command': today}})
                logger.info('User added in mdb after select /start command')
            elif mdb.users.find_one({'user_id': user['id']}) is not None:
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'selected /start command': today}})
                logger.info('In mdb updated date and time user select /start command')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_start() function', traceback=True)

    @staticmethod
    def add_db_help(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время вызова команды /help пользователя Telegram в массив с ключом
        "selected /help command" коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            if mdb.users.find_one({'user_id': user['id']}) is None:
                mdb.users.insert_one(DB.create_collection(user))
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'selected /help command': today}})
                logger.info('User added in mdb after select /help command')
            elif mdb.users.find_one({'user_id': user['id']}) is not None:
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'selected /help command': today}})
                logger.info('In mdb updated date and time user select /help command')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_help() function', traceback=True)

    @staticmethod
    def add_db_messages(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время отправки пользователем приветственного сообщения в массив с ключом
        "sent a welcome text message" коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            if mdb.users.find_one({'user_id': user['id']}) is None:
                mdb.users.insert_one(DB.create_collection(user))
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'sent a welcome text message': today}})
                logger.info('User added in mdb after send a welcome text message')
            elif mdb.users.find_one({'user_id': user['id']}) is not None:
                mdb.users.update_one({'user_id': user['id']},
                                     {'$push': {'sent a welcome text message': today}})
                logger.info('In mdb updated date and time user send a welcome text message')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_add_db_messages() function', traceback=True)

    @staticmethod
    def add_db_radioactive_monitoring(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Радиационный мониторирг" в массив с
        ключом "press button 'Radioactive monitoring'" соответствующего документа коллекции users базы данных users_db
        в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Radioactive monitoring"': today}})
            logger.info('In mdb added date and time user press button "Radioactive monitoring"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_radioactive_monitoring() function', traceback=True)

    @staticmethod
    def add_db_monitoring_points(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Пункты наблюдения" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Observation points"': today}})
            logger.info('In mdb added date and time user press button "Observation points"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_monitoring_points() function', traceback=True)

    @staticmethod
    def add_db_scraper_Brest(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Брестская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Brest region"': today}})
            logger.info('In mdb added date and time user press button "Brest region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Brest() function', traceback=True)

    @staticmethod
    def add_db_scraper_Vitebsk(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Витебская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Vitebsk region"': today}})
            logger.info('In mdb added date and time user press button "Vitebsk region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Vitebsk() function', traceback=True)

    @staticmethod
    def add_db_scraper_Gomel(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Гомельская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Gomel region"': today}})
            logger.info('In mdb added date and time user press button "Gomel region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Gomel() function', traceback=True)

    @staticmethod
    def add_db_scraper_Grodno(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Гродненская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Grodno region"': today}})
            logger.info('In mdb added date and time user press button "Grodno region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Grodno() function', traceback=True)

    @staticmethod
    def add_db_scraper_Minsk(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Минск и Минская область" в массив
        с ключом "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Minsk region"': today}})
            logger.info('In mdb added date and time user press button "Minsk region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Minsk() function', traceback=True)

    @staticmethod
    def add_db_scraper_Mogilev(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Могилевская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Mogilev region"': today}})
            logger.info('In mdb added date and time user press button "Mogilev region"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_scraper_Mogilev() function', traceback=True)

    @staticmethod
    def add_db_geolocation(user: dict[str, any]) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Отправить мою геолокацию" в массив
        с ключом "press button 'Send geolocation'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {'press button "Send geolocation"': today}})
            logger.info('In mdb added date and time user press button "Send geolocation"')
        except ConnectionError:
            logger.exception('ERROR Error connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_geolocation() function', traceback=True)

    @staticmethod
    def __get_db_users_id() -> list[int]:
        """
        Функция возвращает список уникальных id пользователей Telegram-бота из документов коллекции users базы данных
        users_db в MongoDB Atlas

        :return: список значений поля по ключу 'user_id' всех документов коллекции users базы данных users_db в MongoDB
        """
        usersid = mdb.users.distinct("user_id")
        return usersid

    @staticmethod
    def __get_db_users() -> dict[Any]:
        """
        Функция возвращает из документов коллекции users дазы данных users_db в MongoDB Atlas словарь персональных 
        данных пользователей Telegram бота, включая идентификационные данные - user id, first/last/user names

        :return users: словарь персональных данных пользователей Telegram бота, включая идентификационные данные -
        user id, first/last/user names из всех документов коллекции users базы данных users_db в MongoDB Atlas
        """
        users = mdb.users.find()
        return users

    @staticmethod
    def show_users_id(usersid=__get_db_users_id) -> None:
        """
        Функция выводит в консоль id пользователей Telegram-бота из документов коллекции users дазы данных users_db
        в MongoDB Atlas

        :param usersid: результат вызова функции get_db_users_id() - список значений всех документов коллекции users
        базы данных users_db в MongoDB Atlas по ключу 'user_id'

        :return: строковое представление нумерованных значений всех документов коллекции users базы данных users_db в
        MongoDB Atlas по ключу 'user_id'
        """
        for num, userid in enumerate(DB.__get_db_users_id(), 1):
            print(f"iD {num}-го пользователя - {userid}")

    @staticmethod
    def show_users(users=__get_db_users) -> None:
        """
        Функция выводит в консоль User ID, first/last/user names пользователей Telegram-бота из документов коллекции
        users дазы данных users_db в MongoDB Atlas

        :param users: результат вызова функции get_db_users() - словарь персональных данных пользователей Telegram бота,
        включая идентификационные данные - user id, first/last/user names из всех документов коллекции users базы данных
        users_db в MongoDB Atlas

        :return: значенаия полей всех документов коллекции users базы данных users_db в MongoDB Atlas по ключам user_id,
        first_name, last_name и user_name
        """
        for num, users in enumerate(DB.__get_db_users(), 1):
            print(
                f"Персональные данные {num}-го пользователя:\n"
                f"User ID - {users.get('user_id')}\n"
                f"First name - {users.get('first_name')}\n"
                f"Last name - {users.get('last_name')}\n"
                f"User name - {users.get('user_name')}\n\n"
                )


if __name__ == '__main__':
    query = DB(mdb)
    print(query.show_users())
