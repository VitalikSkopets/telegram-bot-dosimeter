import abc


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
