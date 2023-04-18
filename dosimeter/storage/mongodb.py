import abc
from typing import Any

from pymongo import MongoClient
from telegram import User

from dosimeter import config
from dosimeter.config import ASYMMETRIC_ENCRYPTION, CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.encryption import asym_cypher, sym_cypher
from dosimeter.encryption.interface import BaseCryptographer
from dosimeter.storage import manager_admins as manager
from dosimeter.storage.memory import InternalAdminManager
from dosimeter.storage.repository import DocumentRepository

__all__ = ("MongoDataBase", "mongo_atlas__repo")

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class MongoDataBase(DocumentRepository, abc.ABC):
    """Mongo Data Base client."""

    LOG_MSG = "Action '%s' added to Mongo DB."

    def __init__(
        self,
        cypher: BaseCryptographer = (
            asym_cypher if ASYMMETRIC_ENCRYPTION else sym_cypher
        ),
        control: InternalAdminManager = manager,
    ) -> None:
        """Constructor method for initializing objects of the MongoDataBase class."""
        try:
            client: MongoClient = MongoClient(
                config.MONGO_DB_CONNECTION, serverSelectionTimeoutMS=5000
            )
            logger.debug(
                "Reference to cloud Mongo Atlas Database: '%s'"
                % config.MONGO_DB_CONNECTION
            )
            self.mdb = client.users_db
            logger.info(f"Info about server: {client.server_info()}")
        except Exception as ex:
            logger.exception(
                "Unable to connect to the server. Raised exception: %s" % ex
            )
        self.cypher = cypher
        self.manager = control

    def create_collection(self, user: User) -> dict[str, Any]:
        """Method for creating a document base stored in a data collection."""
        current_user: dict[str, Any] = {
            "user_id": user.id,
            "first_name": self.cypher.encrypt(user.first_name),
            "last_name": self.cypher.encrypt(user.last_name),
            "user_name": self.cypher.encrypt(user.username),
            "start command": [],
            "help command": [],
            "sent greeting message": [],
            "radiation monitoring": [],
            "monitoring points": [],
            "sent location": [],
        }
        logger.info("New collection created", user_id=self.manager.get_one(user.id))
        return current_user

    def add_start(self, user: User) -> None:
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
        logger.info(
            self.LOG_MSG % Action.START.value, user_id=self.manager.get_one(user.id)
        )

    def add_help(self, user: User) -> None:
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
        logger.info(
            self.LOG_MSG % Action.HELP.value, user_id=self.manager.get_one(user.id)
        )

    def add_messages(self, user: User) -> None:
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
            self.LOG_MSG % Action.GREETING.value, user_id=self.manager.get_one(user.id)
        )

    def add_radiation_monitoring(self, user: User) -> None:
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
            self.LOG_MSG % Action.MONITORING.value,
            user_id=self.manager.get_one(user.id),
        )

    def add_monitoring_points(self, user: User) -> None:
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
            self.LOG_MSG % Action.POINTS.value, user_id=self.manager.get_one(user.id)
        )

    def add_region(self, user: User, region: Action) -> None:
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
        logger.info(self.LOG_MSG % region.value, user_id=self.manager.get_one(user.id))

    def add_location(self, user: User) -> None:
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
        logger.info(
            self.LOG_MSG % Action.LOCATION.value, user_id=self.manager.get_one(user.id)
        )

    def get_user_by_id(self, user_id: int) -> Any:
        """Method for getting info about the user by id from the database."""
        query = {"user_id": user_id}
        user = self.mdb.users.find_one(query)
        logger.debug(f"Info about the user: {user}")
        return user

    def get_count_of_users(self, user: User | None = None) -> str:
        """Method for getting the number of users from the database."""
        msg = "Users count in the database:"
        users_count = self.mdb.users.count_documents({})
        logger.debug(
            "%s %d" % (msg, users_count),
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return f"{msg} [{users_count}]"

    def get_all_users_ids(self) -> str:
        """
        The method queries the database and outputs a selection of User IDs to the
        console.
        """
        response = [
            f"{num}th user ID: {user_id}"
            for num, user_id in enumerate(self.mdb.users.distinct("user_id"), 1)
        ]
        return "\n".join(response)

    def get_all_users_data(self) -> str:
        """
        The method queries the database and outputs a selection of users to the console.
        """
        response = [
            f"""
            Personal date of the {num}th user:
            ID:         {user_data.get("user_id")}
            First name: {user_data.get("first_name")}
            Last name:  {user_data.get("last_name")}
            User name:  {user_data.get("user_name")}
            """
            for num, user_data in enumerate(self.mdb.users.find(), 1)
        ]
        return "\n\n".join(response)


"""MongoDataBase class instance"""
mongo_atlas__repo = MongoDataBase()


if __name__ == "__main__":
    mongo_atlas__repo = MongoDataBase()
    # print(mongo_atlas__repo.get_user_by_id(413818791))
    # print(mongo_atlas__repo.get_all_users_data())
    # print(mongo_atlas__repo.get_all_users_ids())
    # print(mongo_atlas__repo.get_count_of_users())
