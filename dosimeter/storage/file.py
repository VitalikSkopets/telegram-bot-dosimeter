import abc
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError
from telegram import User

from dosimeter.admin import AdminManager, InternalAdminManager, manager
from dosimeter.config import config
from dosimeter.config.logging import CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.encryption import BaseCryptographer, asym_cypher, sym_cypher
from dosimeter.storage.repository import DocumentType, Repository
from dosimeter.storage.schema import FileCollectionDataSchema
from dosimeter.utils import JSONFileManager

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class FileRepository(Repository, abc.ABC):
    """
    JSON file repository.
    """

    LOG_MSG = "Action '%s' added to the file repo."

    def __init__(
        self,
        path_to_file: Path = config.repo.path,
        cypher: BaseCryptographer = (
            asym_cypher if config.enc.isAsymmetric else sym_cypher
        ),
        control: AdminManager = InternalAdminManager(),
    ) -> None:
        self.repo = JSONFileManager(path_to_file)
        self.cypher = cypher
        self.manager = control

        if Path(self.repo.file).exists() and self.repo.read():
            return

        self.repo.write({"users": []})
        logger.info(f"File repository initialized by path {self.repo.file}")

    def put(self, user: User, action: Action) -> None:
        """
        Method for adding information to the file about the user's call
        to the command.
        """

        if not self._has_user(user.id):
            data = self.repo.read()
            data["users"].append(self._create(user))
            self.repo.write(data)
            logger.info(
                "Data about new user, placed in the collection",
                user_id=self.manager.get_one(user.id),
            )

        if self._has_user(user.id):
            data = self.repo.read()
            for item in data["users"]:
                if user.id == item["user_id"]:
                    if action in item.keys():
                        item[action].append(self._time_stamp())
                    else:
                        item[action] = [self._time_stamp()]
                    self.repo.write(data)
                    logger.info(
                        "Data about user in collection has been updated",
                        user_id=self.manager.get_one(user.id),
                    )
                    break

        logger.info(self.LOG_MSG % action, user_id=self.manager.get_one(user.id))

    def get_users_count(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the file repo.
        """
        data = self.repo.read()
        logger.debug(
            "Users count in the database: %d" % len(data["users"]),
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return len(data["users"])

    def get_user(self, user_id: int) -> DocumentType | None:
        """
        Method for getting info about the user by id from the file repo.
        """
        data = self.repo.read()
        for user in data["users"]:
            if user["user_id"] == user_id:
                logger.debug(f"Info about the user: {user}")
                return user

        return None

    def _has_user(self, user_id: int) -> bool:
        data = self.repo.read()
        user_ids = {user["user_id"] for user in data["users"]}
        return True if user_id in user_ids else False

    def _create(self, user: User) -> DocumentType | None:
        """
        Method for creating a document base stored in a data collection.
        """
        data = {
            "user_id": user.id,
            "first_name": self.cypher.encrypt(user.first_name),
            "last_name": self.cypher.encrypt(user.last_name),
            "user_name": self.cypher.encrypt(user.username),
            "create_at": self._time_stamp(),
        }
        try:
            collection = FileCollectionDataSchema(**data)  # type: ignore[arg-type]
        except ValidationError as exc:
            logger.exception(
                "Validation error. Raised exception: %s" % exc,
                user_id=self.manager.get_one(user.id) if user else None,
            )
            collection = None
        logger.info(
            "New collection created",
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return collection.dict() if collection else None

    @staticmethod
    def _time_stamp() -> str:
        return datetime.now().strftime(config.app.date_format)


if __name__ == "__main__":
    import os

    file_repo = FileRepository()
    file_repo.get_user(int(os.environ["MAIN_ADMIN_TGM_ID"]))
    file_repo.get_users_count()
