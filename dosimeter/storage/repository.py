import abc

from telegram import User

from dosimeter.constants import Action

__all__ = ("AdminManager", "Repository")


class Repository(abc.ABC):
    @abc.abstractmethod
    def put(self, user: User, action: Action) -> None:
        """
        Method that adds to the repository information about the user's use of the
        command.
        """
        pass

    @abc.abstractmethod
    def get_count_of_users(self, user: User | None = None) -> int:
        """
        Method for getting the number of users from the database.
        """
        pass


class AdminManager(abc.ABC):
    @abc.abstractmethod
    def get_one(self, uid: str | int | None = None) -> str | int | None:
        """
        The method returns a digital ID or the string "ADMIN" from the admin`s repo.
        """
        pass

    @abc.abstractmethod
    def get_all(self) -> list[tuple[int, int]] | str | None:
        """
        The method returns a numbered list of admin IDs from the admin repository.
        """
        pass

    @abc.abstractmethod
    def add(self, uid: int) -> tuple[str, bool]:
        """
        A method for adding a digital ID to the list of admin IDs in the admin`s repo.
        """
        pass

    @abc.abstractmethod
    def delete(self, uid: int) -> tuple[str, bool]:
        """
        A method for deleting a digital ID in the list of admin IDs in the admin`s repo.
        """
        pass
