import abc

from telegram import User

from telegram_bot_dosimeter.constants import Action

__all__ = ("DocumentRepository",)


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
