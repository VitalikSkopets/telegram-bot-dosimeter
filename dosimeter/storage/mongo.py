import abc
from datetime import datetime
from typing import ParamSpec

from pydantic import ValidationError
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ConnectionFailure
from telegram import User

from dosimeter.admin import AdminManager, InternalAdminManager, manager
from dosimeter.config import config
from dosimeter.config.logging import CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.encryption import BaseCryptographer, asym_cypher, sym_cypher
from dosimeter.storage.repository import DocumentType, Repository
from dosimeter.storage.schema import MongoCollectionDataSchema

P = ParamSpec("P")

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class CloudMongoDataBase(Repository, abc.ABC):
    """
    Cloud Mongo Atlas Database repository.
    """

    LOG_MSG = "Action '%s' added to Mongo DB."
    __instance = None

    def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> "CloudMongoDataBase":
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
        control: AdminManager = InternalAdminManager(),
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

    def put(self, user: User, action: Action) -> None:
        """
        Method for adding information to the database about the user's call
        to the command.
        """
        if not self.mdb.users.find_one({"user_id": user.id}):
            self.mdb.users.insert_one(self._create(user))
        self._update(user.id, action)
        logger.info(self.LOG_MSG % action, user_id=self.manager.get_one(user.id))

    def get_count(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the database.
        """
        users_count = self.mdb.users.count_documents({})
        logger.debug(
            "Users count in the database: %d" % users_count,
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return users_count

    def get(self, user_id: int | str) -> DocumentType | str:
        """
        Method for getting info about the user by id from the database.
        """
        notification = "User does not exist."
        query = {"user_id": int(user_id)}
        user = self.mdb.users.find_one(query)
        logger.debug(f"Info about the user: {user if user else notification}")
        return user if user else notification

    def get_ids(self) -> str:
        """
        The method queries the database and outputs a selection of User IDs to the
        console.
        """
        response = [
            f"{num}th user ID: {user_id}"
            for num, user_id in enumerate(self.mdb.users.distinct("user_id"), 1)
        ]
        return "\n".join(response)

    def get_data(self) -> str:
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

    def _create(self, user: User) -> DocumentType | None:
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
            collection = MongoCollectionDataSchema(**data)
        except ValidationError as exc:
            logger.exception(
                "Validation error. Raised exception: %s" % exc,
                user_id=self.manager.get_one(user.id) if user else None,
            )
            collection = None
        logger.info("New collection created", user_id=self.manager.get_one(user.id))
        return collection.dict() if collection else None

    def _update(self, user_id: int, field: str) -> None:
        """
        Private method for adding the current date of the corresponding field of the
        data collection.
        """
        self.mdb.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    field: datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                },
            },
        )


if __name__ == "__main__":
    import os

    mongo_cloud = CloudMongoDataBase()
    mongo_cloud.get(os.environ["MAIN_ADMIN_TGM_ID"])
    logger.debug(mongo_cloud.get_data())
    logger.debug(mongo_cloud.get_ids())
    mongo_cloud.get_count()
