import abc
from datetime import datetime
from typing import Any, Mapping, TypeAlias, TypeVar

from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from telegram import User

from dosimeter.config import db_settings, settings
from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.encryption import asym_cypher, sym_cypher
from dosimeter.encryption.interface import BaseCryptographer
from dosimeter.storage import manager_admins as manager
from dosimeter.storage.memory import InternalAdminManager
from dosimeter.storage.repository import Repository

__all__ = ("MongoDataBase", "mongo_atlas__repo")

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})

Date: TypeAlias = str
CollectionType: TypeAlias = dict[str, Any]
DocumentType = TypeVar("DocumentType", bound=Mapping[str, Any])


# noinspection PyMethodParameters
class CollectionDataSchema(BaseModel):
    """
    Schema for data documents collection in Mongo DB.
    """

    user_id: int
    first_name: str
    last_name: str
    user_name: str
    start_command: list[Date] = []
    help_command: list[Date] = []
    donate_command: list[Date] = []
    sent_greeting_message: list[Date] = []
    radiation_monitoring: list[Date] = []
    monitoring_points: list[Date] = []
    sent_location: list[Date] = []

    @validator(
        "start_command",
        "help_command",
        "donate_command",
        "sent_greeting_message",
        "radiation_monitoring",
        "monitoring_points",
        "sent_location",
        each_item=True,
    )
    def check_date(cls, value: Date) -> Date:
        if not isinstance(value, str):
            raise TypeError("date must be a string.")
        else:
            try:
                datetime.strptime(value, "%d-%b-%Y")
                return value
            except ValueError:
                raise ValueError("date must be %d-%b-%Y format.")


class MongoDataBase(Repository, abc.ABC):
    """
    Mongo Data Base client.
    """

    LOG_MSG = "Action '%s' added to Mongo DB."

    def __init__(
        self,
        cypher: BaseCryptographer = (
            asym_cypher if settings.ASYMMETRIC_ENCRYPTION else sym_cypher
        ),
        control: InternalAdminManager = manager,
    ) -> None:
        """
        Constructor method for initializing objects of the MongoDataBase class.
        """
        try:
            client: MongoClient = MongoClient(
                db_settings.mongo_url, serverSelectionTimeoutMS=5000
            )
            logger.debug(
                "Reference to cloud Mongo Atlas Database: '%s'" % db_settings.mongo_url
            )
            self.mdb = client.users_db
            logger.info(f"Info about server: {client.server_info()}")
        except Exception as ex:
            logger.exception(
                "Unable to connect to the server. Raised exception: %s" % ex
            )
        self.cypher = cypher
        self.manager = control

    def create(self, user: User) -> CollectionType | None:
        """
        Method for creating a document base stored in a data collection.
        """
        data = {
            "user_id": user.id,
            "first_name": self.cypher.encrypt(user.first_name),
            "last_name": self.cypher.encrypt(user.last_name),
            "user_name": self.cypher.encrypt(user.username),
        }
        try:
            collection = CollectionDataSchema(**data)
        except ValidationError as ex:
            logger.exception("Validation error. Raised exception: %s" % ex)
            collection = None
        if not collection:
            return None
        logger.info("New collection created", user_id=self.manager.get_one(user.id))
        return collection.dict()

    def put(self, user: User, action: Action) -> None:
        """
        Method for adding information to the database about the user's call
        to the command.
        """
        if not self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.insert_one(self.create(user))
        self._update(user.id, action)
        logger.info(self.LOG_MSG % action, user_id=self.manager.get_one(user.id))

    def get_count_of_users(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the database.
        """
        users_count = self.mdb.users.count_documents({})
        logger.debug(
            "Users count in the database: %d" % users_count,
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return users_count

    def get_user_by_id(self, user_id: int) -> DocumentType | None:
        """
        Method for getting info about the user by id from the database.
        """
        query = {"user_id": user_id}
        user = self.mdb.users.find_one(query)
        logger.debug(f"Info about the user: {user}")
        return user

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

    def _update(self, user_id: int, field: str) -> None:
        """
        Private method for adding the current date of the corresponding field of the
        data collection.
        """
        self.mdb.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    field: settings.DATE,
                },
            },
        )


"""MongoDataBase class instance"""
mongo_atlas__repo = MongoDataBase()


if __name__ == "__main__":
    mongo_atlas__repo = MongoDataBase()
    # print(mongo_atlas__repo.get_user_by_id(413818791))
    # print(mongo_atlas__repo.get_all_users_data())
    # print(mongo_atlas__repo.get_all_users_ids())
    # print(mongo_atlas__repo.get_count_of_users())
