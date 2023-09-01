import abc
from typing import Mapping, TypeAlias

from telegram import User

from dosimeter.constants import Action

DocumentType: TypeAlias = Mapping[str, int | str | None | list[str]]


class Repository(abc.ABC):
    """
    Abstract repository (storage) class.
    """

    @abc.abstractmethod
    def put(self, user: User, action: Action) -> None:
        """
        Method that adds to the repository information about the user's use of the
        command.
        """
        pass

    @abc.abstractmethod
    def get_count(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the database.
        """
        pass

    @abc.abstractmethod
    def get(self, user_id: int | str) -> DocumentType | str:
        """
        Method for getting info about the user by id from the database.
        """
        pass

    @abc.abstractmethod
    def _create(self, user: User) -> DocumentType | None:
        """
        Method for creating a document base stored in a data collection.
        """
        pass
