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
    Class for representation JSON file repository.
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
        """
        Instantiate a FileRepository instance.
        """

        self.repo = JSONFileManager(path_to_file)
        self.cypher = cypher
        self.manager = control

        if Path(self.repo.file).exists() and self.repo.read():
            return

        self.repo.write({"users": []})
        logger.info("File repository initialized by path %s" % self.repo.file)

    def __str__(self) -> str:
        """
        Method returns a printable string representation
        of an instantiated object of the FileRepository class.
        """
        return "File repository by path: %s" % self.repo.file

    def put(self, user: User, action: Action) -> None:
        """
        Method for adding information to the file
        about the user's call to the command.
        """

        if not self._has_user(user.id):
            data = self.repo.read()
            data["users"].append(self._create(user))
            self.repo.write(data)
            logger.info(
                "Data about new user, placed in the collection",
                user_id=self.manager.get_one(user.id),
            )

        self._update(user.id, action)
        logger.info(self.LOG_MSG % action, user_id=self.manager.get_one(user.id))

    def get_count(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the file repo.
        """
        data = self.repo.read()
        logger.debug(
            "Users count in the database: %d" % len(data["users"]),
            user_id=self.manager.get_one(user.id) if user else None,
        )
        return len(data["users"])

    def get(self, user_id: int | str) -> DocumentType | str:  # type: ignore[return]
        """
        Public method for getting info about the user by id from the file repo.
        """
        match user_id:
            case int() as idf if idf >= 0:
                return self._obtain(idf)
            case str() as idf if idf.strip().isdigit():
                return self._obtain(int(idf))
            case str() as idf if not idf.strip().isdigit():
                raise ValueError("The string must consist of digits.")
            case _:
                raise ValueError("ID must be an integer, a positive number.")

    def _has_user(self, user_id: int) -> bool:
        """
        Private method for checking if user information is available in the database.
        """
        data = self.repo.read()
        user_ids = {user["user_id"] for user in data["users"]}
        return True if user_id in user_ids else False

    def _create(self, user: User) -> DocumentType | None:
        """
        Private method for creating a document base stored in a data collection.
        """
        data = {
            "user_id": user.id,
            "first_name": self.cypher.encrypt(user.first_name),
            "last_name": self.cypher.encrypt(user.last_name),
            "user_name": self.cypher.encrypt(user.username),
            "create_at": self._time_stamp(),
        }
        try:
            collection = FileCollectionDataSchema(**data)
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

    def _obtain(self, idf: int) -> DocumentType | str:
        """
        Private method for obtaining user object by id from the file repository.
        """
        data = self.repo.read()
        for user in data["users"]:
            if user["user_id"] == idf:
                logger.debug(f"Info about the user: {user}")
                return user
        return "User does not exist."

    def _update(self, idf: int, action: Action) -> None:
        """
        Private method for adding info about a user's action to the file storage.
        """
        data = self.repo.read()
        for item in data["users"]:
            if idf == item["user_id"]:
                if action in item.keys():
                    item[action].append(self._time_stamp())
                else:
                    item[action] = [self._time_stamp()]
                self.repo.write(data)

    @staticmethod
    def _time_stamp() -> str:
        """
        Static method that returns a string object of the current date
        and time in a specific format.
        """
        return datetime.now().strftime(config.app.date_format)


if __name__ == "__main__":
    import os

    file_repo = FileRepository()
    file_repo.get(os.environ["MAIN_ADMIN_TGM_ID"])
    file_repo.get_count()
