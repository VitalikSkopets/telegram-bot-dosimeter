from pathlib import Path
from typing import Union

from dosimeter.config import settings
from dosimeter.constants import ADMIN_ID, LIST_OF_ADMIN_IDS, Files
from dosimeter.encryption import asym_cypher, sym_cypher
from dosimeter.encryption.asymmetric import AsymmetricCryptographer
from dosimeter.encryption.symmetric import SymmetricCryptographer
from dosimeter.storage.repository import AdminManager

__all__ = ("FileAdminManager",)


class FileAdminManager(AdminManager):
    """A class that encapsulates the logic of managing the list of administrators
    stored in a file."""

    FILE_PATH = Files.ADMINS_FILE_PATH
    LIST_OF_ADMINS = LIST_OF_ADMIN_IDS

    def __init__(
        self,
        cryptographer: Union[SymmetricCryptographer, AsymmetricCryptographer] = (
            asym_cypher if settings.ASYMMETRIC_ENCRYPTION else sym_cypher
        ),
    ) -> None:
        self.cryptographer = cryptographer
        self.temp_list_admins = [*self.LIST_OF_ADMINS]
        if Path(self.FILE_PATH).exists():
            return
        with open(self.FILE_PATH, "w+") as file:
            for uid in self.temp_list_admins:
                file.write(f"{self.cryptographer.encrypt(str(uid))}" + "\n")

    def get_one(self, uid: str | int | None = None) -> str | int | None:
        """The method returns a numeric identifier or the string "ADMIN" from
        the temporary list of administrators stored in the file."""
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
        if uid and str(uid) not in admins:
            return int(uid)
        if uid and str(uid) in admins:
            return "ADMIN"
        return None

    def get_all(self) -> str:
        """The method returns a string representation of the numbered
        list of admins IDs from the temporary list of administrators stored in the file.
        """
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
        if not admins:
            return "Admins not assigned"
        output = []
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
            for num, uid in enumerate(admins, 1):
                message = "{}: {} - Main admin" if uid == str(ADMIN_ID) else "{}: {}"
                output.append(message.format(num, uid))
        return "\n".join(output)

    def add(self, uid: int) -> tuple[str, bool]:
        """A method for adding a digital user ID to a file with a temporary
        list of administrator IDs."""
        with open(self.FILE_PATH, "r") as file:
            admins = file.read()
        if str(uid) in admins.split():
            return "The user ID has already been added to the list of admins.", False
        with open(self.FILE_PATH, "a") as file:
            file.write(f"{self.cryptographer.encrypt(str(uid))}" + "\n")
        return f"User ID <u>{uid}</u> added to the list of admins.", True

    def delete(self, uid: int) -> tuple[str, bool]:
        """A method for deleting a digital user ID from a file with a temporary
        list of administrator IDs."""
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]

        if str(uid) not in admins:
            return "This user ID is not in the list of administrators.", False

        admins.remove(str(uid))

        with open(self.FILE_PATH, "w") as file:
            for admin_id in admins:
                file.write(f"{self.cryptographer.encrypt(str(admin_id))}" + "\n")

        return f"User ID <u>{str(uid)}</u> deleted to the list of admins.", True
