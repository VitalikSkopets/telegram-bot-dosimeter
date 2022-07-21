from typing import Any

from pymongo import MongoClient
from telegram import User

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.crypto import DataEncrypt
from telegram_bot_dosimeter.logging_config import get_logger
from telegram_bot_dosimeter.storage.repository import DocumentRepository

__all__ = ("MongoDataBase",)

logger = get_logger(__name__)

client_mdb: MongoClient = MongoClient(
    config.MONGO_DB_LINK, serverSelectionTimeoutMS=5000
)


class MongoDataBase(DocumentRepository):
    """MongoDB client."""

    def __init__(self, client: MongoClient = client_mdb) -> None:
        """Constructor method for initializing objects of the MongoDataBase class."""
        try:
            self.mdb = client.users_db
            logger.info(f"Info about server: {client.server_info()}")
        except Exception as ex:
            logger.error(f"Unable to connect to the server. Raised exception: {ex}")

    @staticmethod
    def create_collection(user: User) -> dict[str, Any]:
        """Method for creating a document base stored in a data collection."""
        first_name: DataEncrypt = DataEncrypt(user.first_name)
        last_name: DataEncrypt = DataEncrypt(user.last_name)  # type: ignore
        user_name: DataEncrypt = DataEncrypt(user.username)  # type: ignore

        current_user: dict[str, Any] = {
            "user_id": user.id,
            "first_name": first_name.encrypt(),
            "last_name": last_name.encrypt(),
            "user_name": user_name.encrypt(),
            "start command": [],
            "help command": [],
            "sent greeting message": [],
            "radiation monitoring": [],
            "monitoring points": [],
            "sent location": [],
        }
        logger.info("Collection created")
        return current_user

    def add_start(self, user: User) -> Any:
        """
        Method for adding information to the database about the user's call to the
        Start command.
        """
        if not self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.insert_one(self.create_collection(user))
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        "start command": config.TODAY,
                    },
                },
            )
        if self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        "start command": config.TODAY,
                    },
                },
            )
        logger.info(f"Info about action 'Start command' by user {user.id} added to DB.")

    def add_help(self, user: User) -> Any:
        """
        Method for adding information to the database about the user calling the Help
        command.
        """
        if not self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.insert_one(self.create_collection(user))
            self.mdb.users.update_one(
                {"user_id": user.id},
                {"$push": {"help command": config.TODAY}},
            )
        if self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        "help command": config.TODAY,
                    },
                },
            )
        logger.info(f"Info about action 'Help command' by user {user.id} added to DB.")

    def add_messages(self, user: User) -> Any:
        """
        Method for adding to the database information about the user sending a
        greeting message.
        """
        if not self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.insert_one(self.create_collection(user))
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        "sent greeting message": config.TODAY,
                    },
                },
            )
        if self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.update_one(
                {"user_id": user.id},
                {
                    "$push": {
                        "sent greeting message": config.TODAY,
                    },
                },
            )
        logger.info(
            f"Info about action 'Greeting message sent' by user {user.id} added to DB."
        )

    def add_radiation_monitoring(self, user: User) -> Any:
        """
        Method for adding information about a user who used Radiation Monitoring to
        the database.
        """
        self.mdb.users.update_one(
            {"user_id": user.id},
            {
                "$push": {
                    "radiation monitoring": config.TODAY,
                },
            },
        )
        logger.info(
            f"Info about action 'Radiation monitoring' by user {user.id} added to DB."
        )

    def add_monitoring_points(self, user: User) -> Any:
        """
        Method for adding information about a user who used Monitoring Points to the
        database.
        """
        self.mdb.users.update_one(
            {"user_id": user.id},
            {
                "$push": {
                    "monitoring points": config.TODAY,
                },
            },
        )
        logger.info(
            f"Info about action 'Monitoring points' by user {user.id} added to DB."
        )

    def add_region(self, user: User, region: str) -> Any:
        """
        Method for adding information about a user who used Region to the database.
        """
        self.mdb.users.update_one(
            {"user_id": user.id},
            {
                "$push": {
                    f"{region}": config.TODAY,
                },
            },
        )
        logger.info(f"Info about action '{region}' by user {user.id} added to DB.")

    def add_location(self, user: User) -> Any:
        """
        Method for adding information about the user who sent his geolocation to the
        database.
        """
        self.mdb.users.update_one(
            {"user_id": user.id},
            {
                "$push": {
                    "sent location": config.TODAY,
                },
            },
        )
        logger.info(f"Info about action 'Sent location' by user {user.id} added to DB.")

    def get_user_by_id(self, user_id: int) -> Any:
        """Method for getting info about the user by id from the database."""
        query = {"user_id": user_id}
        print(self.mdb.users.find_one(query))

    def get_users_count(self) -> Any:
        """Method for getting the number of users from the database."""
        print(self.mdb.users.count_documents({}))

    def get_all_users_ids(self) -> Any:
        """
        The method queries the database and outputs a selection of User IDs to the
        console.
        """
        for num, user_id in enumerate(  # type: ignore
            self.mdb.users.distinct("user_id"), 1
        ):
            print(f"{num}th user ID: {user_id}")

    def get_all_users_data(self) -> Any:
        """
        The method queries the database and outputs a selection of users to the console.
        """
        for num, user_data in enumerate(self.mdb.users.find(), 1):  # type: ignore
            print(
                f"""
                Personal date of the {num}th user:
                ID:         {user_data.get("user_id")}
                First name: {user_data.get("first_name")}
                Last name:  {user_data.get("last_name")}
                User name:  {user_data.get("user_name")}
                """
            )


if __name__ == "__main__":
    session = MongoDataBase(client_mdb)
    print(session.get_user_by_id(413818791))
    print(session.get_all_users_data())
    print(session.get_all_users_ids())
    print(session.get_users_count())
