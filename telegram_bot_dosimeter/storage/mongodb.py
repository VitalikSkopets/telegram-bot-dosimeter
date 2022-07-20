from typing import Any

from pymongo import MongoClient
from telegram import User

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.crypto import DataEncrypt
from telegram_bot_dosimeter.logging_config import get_logger
from telegram_bot_dosimeter.storage.repository import DocumentRepository

__all__ = ("MongoDataBase",)

logger = get_logger(__name__)

client_mdb: MongoClient = MongoClient(config.MONGO_DB_LINK)


class MongoDataBase(DocumentRepository):
    """
    MongoDB client.
    """

    def __init__(self, client: MongoClient = client_mdb) -> None:
        """
        Constructor method for initializing objects of the MongoDataBase class.
        :param client: object pymongo.MongoClient class for connection with users_db
        in MongoDB Atlas
        """
        try:
            self.mdb = client
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    @staticmethod
    def create_collection(user: User) -> dict[str, Any]:
        """
        Метод создает объект с типом данных "словарь", содержащий в качестве ключей
        "идентификационные данные пользователя" и доступный перечень "действий" бота.
        Значения ключей first_name, last_name и username добавляются в словарь в
        зашифрованном виде с использованием метода encrypt() из класса DataEncrypt,
        а значениями "действий" бота являются пустые массивы (списки), в которые
        впоследствии будут добавлятся дата и время их совершения.
        :param user: object telegram.User class with information about user
        :return: словарь current_user, являющийся схемой документа для добавления в
        коллекцию users БД users_db в MongoDB
        """
        first_name: DataEncrypt = DataEncrypt(user.first_name)
        last_name: DataEncrypt = DataEncrypt(user.last_name)  # type: ignore
        user_name: DataEncrypt = DataEncrypt(user.username)  # type: ignore

        current_user: dict[str, Any] = {
            "user_id": user.id,
            "first_name": first_name.encrypt(),
            "last_name": last_name.encrypt(),
            "user_name": user_name.encrypt(),
            "selected /start command": [],
            "selected /help command": [],
            "sent a welcome text message": [],
            'press button "Radioactive monitoring"': [],
            'press button "Observation points"': [],
            'press button "Send geolocation"': [],
        }
        return current_user

    def add_start(self, user: User) -> Any:
        """
        Метод добавляет дату и время вызова пользователем команды /start
        в массив с ключом "selected /start command" коллекции users users_db
        в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            if not self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.insert_one(self.create_collection(user))
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"selected /start command": config.TODAY}},
                )
                logger.info("User added in mdb after select /start command")
            if self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"selected /start command": config.TODAY}},
                )
                logger.info("In mdb updated date and time user select /start command")
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_help(self, user: User) -> Any:
        """
        Метод добавляет текущую дату и время вызова команды /help пользователя
        Telegram в массив с ключом "selected /help command" коллекции users users_db
        в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            if not self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.insert_one(self.create_collection(user))
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"selected /help command": config.TODAY}},
                )
                logger.info("User added in mdb after select /help command")
            if self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"selected /help command": config.TODAY}},
                )
                logger.info("In mdb updated date and time user select /help command")
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_messages(self, user: User) -> Any:
        """
        Метод добавляет дату и время отправки пользователем приветственного
        сообщения в массив с ключом "sent a welcome text message" коллекции users
        users_db в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            if not self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.insert_one(self.create_collection(user))
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"sent a welcome text message": config.TODAY}},
                )
                logger.info("User added in mdb after send a welcome text message")
            if self.mdb.users.find_one({"user_id": user.id}):
                self.mdb.users.update_one(
                    {"user_id": user.id},
                    {"$push": {"sent a welcome text message": config.TODAY}},
                )
                logger.info(
                    "In mdb updated date and time user send a welcome text message"
                )
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_radiation_monitoring(self, user: User) -> Any:
        """
        Метод добавляет дату и время использования пользователем кнопки
        "Радиационный мониторирг" в массив с ключом "press button 'Radioactive
        monitoring'" соответствующего документа коллекции users базы данных users_db
        в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            self.mdb.users.update_one(
                {"user_id": user.id},
                {"$push": {'press button "Radioactive monitoring"': config.TODAY}},
            )
            logger.info(
                'In mdb added date and time user press button "Radioactive monitoring"'
            )
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_monitoring_points(self, user: User) -> Any:
        """
        Метод добавляет дату и время использования пользователем кнопки
        "Пункты наблюдения" в массив с ключом "press button 'Observation points'"
        соответствующего документа коллекции users users_db в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            self.mdb.users.update_one(
                {"user_id": user.id},
                {"$push": {'press button "Observation points"': config.TODAY}},
            )
            logger.info(
                'In mdb added date and time user press button "Observation points"'
            )
        except ConnectionError:
            logger.exception("Connecting error to the database.")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_region(self, user: User, region: str) -> Any:
        """
        Метод добавляет дату и время использования пользователем кнопки
        "Брестская область" в массив с ключом "press button 'Observation points'"
        соответствующего документа коллекции users users_db в MongoDB Atlas.
        :param region: строковый объект - наименование региона, которое передается
        при выполнении метода scraper_*() класса Callback
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            self.mdb.users.update_one(
                {"user_id": user.id},
                {"$push": {f'press button "{region}"': config.TODAY}},
            )
        except ConnectionError:
            logger.exception("Connecting error to the database")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def add_location(self, user: User) -> Any:
        """
        Метод добавляет текущую дату и время использования пользователем кнопки
        "Отправить мою геолокацию" в массив с ключом "press button 'Send
        location'" соответствующего документа коллекции users users_db в MongoDB Atlas.
        :param user: object telegram.User class with information about user
        :return: None
        """
        try:
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        'press button "Send geolocation"': config.TODAY,
                    }
                },
            )
            logger.info(
                'Into DataBase added date and time user press button "Send location"'
            )
        except ConnectionError:
            logger.exception("Connecting error to the database")
        except Exception as ex:
            logger.error(f"Raised exception {ex}")

    def show_users_id(self) -> Any:
        """
        Метод запрашивает из базы данных и выводит в консоль выборку id
        пользователей Telegram-бота из документов коллекции users базы данных
        users_db в MongoDB Atlas.
        :return: строковое представление нумерованных значений всех документов
        коллекции users базы данных users_db в MongoDB Atlas по ключу 'user_id'
        """
        for num, user_id in enumerate(  # type: ignore
            self.mdb.users.distinct("user_id"), 1
        ):
            print(f"{num}th user ID - {user_id}")

    def show_users_data(self) -> Any:
        """
        Метод запрашивает из базы данных и выводит в консоль выборку User ID,
        first/last/user names пользователей Telegram-бота из документов коллекции
        users базы данных users_db в MongoDB Atlas.
        :return: значенаия полей всех документов коллекции users базы данных users_db
        в MongoDB Atlas по ключам user_id, first_name, last_name и user_name
        """
        for num, user_data in enumerate(self.mdb.users.find(), 1):  # type: ignore
            print(
                f"""
                Personal date of the {num}th user:\n
                ID - {user_data.get("user_id")}\n
                First name - {user_data.get("first_name")}\n
                Last name - {user_data.get("last_name")}\n
                User name - {user_data.get("user_name")}\n\n
                """
            )


if __name__ == "__main__":
    query = MongoDataBase(client_mdb)
    print(query.show_users_data())
    print(query.show_users_id())
