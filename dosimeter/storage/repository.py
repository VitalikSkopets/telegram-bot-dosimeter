import abc

from telegram import User

from dosimeter.constants import Action


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
