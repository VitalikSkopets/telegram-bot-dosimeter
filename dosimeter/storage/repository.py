import abc

from telegram import User

from dosimeter.constants import Action

__all__ = ("AdminManager", "DocumentRepository")


class DocumentRepository(abc.ABC):
    @abc.abstractmethod
    def add_start(self, user: User) -> None:
        """
        Method that adds to the repository information about the user's use of the
        Start command.
        """
        pass

    @abc.abstractmethod
    def add_help(self, user: User) -> None:
        """
        Method that adds to the repository information about the user's use of the
        Help command.
        """
        pass

    @abc.abstractmethod
    def add_messages(self, user: User) -> None:
        """
        Method that adds to the repository the information that the user bot has a
        text message.
        """
        pass

    @abc.abstractmethod
    def add_radiation_monitoring(self, user: User) -> None:
        """
        Method that adds to the repository information about the user's use of the
        Radiation monitoring command.
        """
        pass

    @abc.abstractmethod
    def add_monitoring_points(self, user: User) -> None:
        """
        Method that adds to the repository information about the user's use of the
        Monitoring points command.
        """
        pass

    @abc.abstractmethod
    def add_region(self, user: User, region: Action) -> None:
        """
        Method that adds information to the repository that the user used a command
        to select the appropriate region.
        """
        pass

    @abc.abstractmethod
    def add_location(self, user: User) -> None:
        """
        Method that adds to the repository information about the user's use of the
        Send location command.
        """
        pass

    @abc.abstractmethod
    def get_count_of_users(self, user: User | None = None) -> str:
        """Method for getting the number of users from the database."""
        pass


class AdminManager(abc.ABC):
    @abc.abstractmethod
    def get_one(self, uid: str | int | None = None) -> str | int | None:
        """
        The method returns a digital ID or the string "ADMIN" from the admin`s repo.
        """
        pass

    @abc.abstractmethod
    def get_all(self) -> str:
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
