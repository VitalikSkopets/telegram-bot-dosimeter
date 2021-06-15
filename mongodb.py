from pymongo import MongoClient
from config import today, mdb
from crypto import Crypt
from loguru import logger


class DB:

    def __init__(self, mdb: MongoClient):
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
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database. Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_start() function. Exception is {ex}', traceback=True)

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
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database. Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_help() function. Exception is {ex}', traceback=True)

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
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database. Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_add_db_messages() function. Exception is {ex}',
                             traceback=True)

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
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database. Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_radioactive_monitoring() function. Exception is {ex}',
                             traceback=True)

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
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database. Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_monitoring_points() function. Exception is {ex}',
                             traceback=True)

    @staticmethod
    def add_db_scraper_region(user: dict[str, any], region: str) -> None:
        """
        Функция добавляет текущую дату и время при нажатии пользователем кнопки "Брестская область" в массив с ключом
        "press button 'Observation points'" соответствующего документа коллекции users users_db в MongoDB Atlas

        :param region: строковый объект - наименование региона, которое передается при выполнении метода scraper_*()
        класса Handlers

        :param user: словарь update.effective_user с информацией о пользователе Telegram

        :return: None
        """
        try:
            mdb.users.update_one({'user_id': user['id']},
                                 {'$push': {f'press button "{region}"': today}})
        except ConnectionError as ex:
            logger.exception(f'ERROR connecting to database, Exception is {ex}', traceback=True)
        except Exception as ex:
            logger.exception(f'ERROR while performing the add_db_scraper_Brest() function. Exception is {ex}',
                             traceback=True)

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
            logger.exception('ERROR connecting to database', traceback=True)
        except Exception:
            logger.exception('ERROR while performing the add_db_geolocation() function', traceback=True)

    @staticmethod
    def show_users_id() -> None:
        """
        Функция запрашивает выборку из базы данных и выводит в консоль id пользователей Telegram-бота из документов
        коллекции users дазы данных users_db в MongoDB Atlas

        :return: строковое представление нумерованных значений всех документов коллекции users базы данных users_db
        в MongoDB Atlas по ключу 'user_id'
        """
        for num, userid in enumerate(mdb.users.distinct("user_id"), 1):
            print(f"iD {num}-го пользователя - {userid}")

    @staticmethod
    def show_users_data() -> None:
        """
        Функция запрашивает выборку из базы данных и выводит в консоль User ID, first/last/user names пользователей
        Telegram-бота из документов коллекции users дазы данных users_db в MongoDB Atlas

        :return: значенаия полей всех документов коллекции users базы данных users_db в MongoDB Atlas по ключам user_id,
        first_name, last_name и user_name
        """
        for num, users_data in enumerate(mdb.users.find(), 1):
            print(
                f"Персональные данные {num}-го пользователя:\n"
                f"User ID - {users_data.get('user_id')}\n"
                f"First name - {users_data.get('first_name')}\n"
                f"Last name - {users_data.get('last_name')}\n"
                f"User name - {users_data.get('user_name')}\n\n"
                )


if __name__ == '__main__':
    query = DB(mdb)
    print(query.show_users_data())
    print(query.show_users_id())
