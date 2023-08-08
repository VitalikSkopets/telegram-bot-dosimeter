import abc
from datetime import datetime
from typing import Any, Mapping, TypeAlias, TypeVar

from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ConnectionFailure
from telegram import User

from dosimeter.config import config
from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.encryption import asym_cypher, sym_cypher
from dosimeter.encryption.interface import BaseCryptographer
from dosimeter.storage import manager_admins as manager
from dosimeter.storage.memory import InternalAdminManager
from dosimeter.storage.repository import Repository

__all__ = ("CloudMongoDataBase", "mongo_cloud")

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
        try:
            datetime.strptime(value, "%d-%b-%Y")
            return value
        except ValueError:
            raise ValueError("date must be %d-%b-%Y format")


class CloudMongoDataBase(Repository, abc.ABC):
    """
    Cloud Mongo Database client.
    """

    LOG_MSG = "Action '%s' added to Mongo DB."
    __instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "CloudMongoDataBase":
        """
        A method that controls the creation of a single instance of the class.
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(
        self,
        cypher: BaseCryptographer = (
            asym_cypher if config.enc.isAsymmetric else sym_cypher
        ),
        control: InternalAdminManager = manager,
    ) -> None:
        """
        Constructor method for initializing objects of the CloudMongoDataBase class.
        """

        def _get_connection() -> Database:
            logger.debug(
                "URI to cloud Mongo Atlas Database Server: '%s'" % config.db.uri
            )
            try:
                client: MongoClient = MongoClient(
                    config.db.uri,
                    serverSelectionTimeoutMS=config.db.timeout,
                    tz_aware=True,
                )
            except (ConnectionFailure, ConfigurationError) as ex:
                logger.exception(
                    "Cloud Server not available. Raised exception: %s" % ex
                )
                raise
            logger.info(f"Info about Server: {client.server_info()}")
            return client.users_db

        self.mdb = _get_connection()
        self.cypher = cypher
        self.manager = control

    def __del__(self) -> None:
        """
        The destructor method that is called before destroying an instance of the class
        and used to clean up memory resources.
        """
        CloudMongoDataBase.__instance = None

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
            collection = CollectionDataSchema(**data)  # type: ignore[arg-type]
        except ValidationError as ex:
            logger.exception("Validation error. Raised exception: %s" % ex)
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
                    field: datetime.today().strftime("%d-%m-%Y %H:%M"),
                },
            },
        )


"""CloudMongoDataBase class instance"""
mongo_cloud = CloudMongoDataBase()


if __name__ == "__main__":
    pass
    # print(mongo_cloud.get_user_by_id(413818791))
    # print(mongo_cloud.get_all_users_data())
    # print(mongo_cloud.get_all_users_ids())
    # print(mongo_cloud.get_count_of_users())
