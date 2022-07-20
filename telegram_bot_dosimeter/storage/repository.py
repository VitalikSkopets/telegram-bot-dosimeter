import abc
from typing import NoReturn

from telegram import User

__all__ = ("DocumentRepository",)


class DocumentRepository(abc.ABC):
    @abc.abstractmethod
    def add_start(self, user: User) -> NoReturn:
        """
        Method that adds to the repository information about the user's use of the
        Start command.
        :param user: object telegram.User class with information about
        user
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_help(self, user: User) -> NoReturn:
        """
        Method that adds to the repository information about the user's use of the
        Help command.
        :param user: object telegram.User class with information about
        user
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_messages(self, user: User) -> NoReturn:
        """
        Method that adds to the repository the information that the user bot has a
        text message.
        :param user: object telegram.User class with information about
        user
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_radiation_monitoring(self, user: User) -> NoReturn:
        """
        Method that adds to the repository information about the user's use of the
        Radiation monitoring command.
        :param user: object telegram.User class with information about
        user
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_monitoring_points(self, user: User) -> NoReturn:
        """
        Method that adds to the repository information about the user's use of the
        Monitoring points command.
        :param user: object telegram.User class with information about
        user
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_region(self, user: User, region: str) -> NoReturn:
        """
        Method that adds information to the repository that the user used a command
        to select the appropriate region.
        :param user: object telegram.User class with information about
        :param region: string object - the name of the region, which is passed when
        executing the scraper_*() method of the object Callback class
        :return: Non-return
        """
        pass

    @abc.abstractmethod
    def add_location(self, user: User) -> NoReturn:
        """
        Method that adds to the repository information about the user's use of the
        Send location command.
        :param user: object telegram.User class with information about user
        :return: Non-return
        """
        pass
