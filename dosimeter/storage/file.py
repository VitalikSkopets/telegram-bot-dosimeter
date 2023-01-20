from pathlib import Path
from typing import Union

from dosimeter.config import ASYMMETRIC_ENCRYPTION
from dosimeter.constants import ADMIN_ID, LIST_OF_ADMIN_IDS, Files
from dosimeter.encryption.asymmetric import AsymmetricCryptographer
from dosimeter.encryption.asymmetric import cryptographer as asym_cypher
from dosimeter.encryption.symmetric import SymmetricCryptographer
from dosimeter.encryption.symmetric import cryptographer as sym_cypher
from dosimeter.storage.repository import AdminManager

__all__ = ("FileAdminManager", "file_manager_admins")


class FileAdminManager(AdminManager):
    FILE_PATH = Files.ADMINS_FILE_PATH
    LIST_OF_ADMINS = LIST_OF_ADMIN_IDS

    def __init__(
        self,
        cryptographer: Union[SymmetricCryptographer, AsymmetricCryptographer] = (
            asym_cypher if ASYMMETRIC_ENCRYPTION else sym_cypher
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
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
        if uid and str(uid) not in admins:
            print(int(uid))
            return int(uid)
        if uid and str(uid) in admins:
            print("ADMIN")
            return "ADMIN"
        return None

    def get_all(self) -> str:
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
        if not admins:
            print("Admins not assigned")
            return "Admins not assigned"
        output = []
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]
            print(admins)
            for num, uid in enumerate(admins, 1):
                message = "{}: {} - Main admin" if uid == str(ADMIN_ID) else "{}: {}"
                output.append(message.format(num, uid))
        print("\n".join(output))
        return "\n".join(output)

    def add(self, uid: int) -> tuple[str, bool]:
        with open(self.FILE_PATH, "r") as file:
            admins = file.read()
        if str(uid) in admins.split():
            print("The user ID has already been added to the list of admins.", False)
            return "The user ID has already been added to the list of admins.", False
        with open(self.FILE_PATH, "a") as file:
            file.write(f"{self.cryptographer.encrypt(str(uid))}" + "\n")
        print(f"User ID <u>{uid}</u> added to the list of admins.", True)
        return f"User ID <u>{uid}</u> added to the list of admins.", True

    def delete(self, uid: int) -> tuple[str, bool]:
        with open(self.FILE_PATH, "r") as file:
            admins = [self.cryptographer.decrypt(line.strip()) for line in file]

        if str(uid) not in admins:
            print("This user ID is not in the list of administrators.", False)
            return "This user ID is not in the list of administrators.", False

        admins.remove(str(uid))

        with open(self.FILE_PATH, "w") as file:
            for admin_id in admins:
                file.write(f"{self.cryptographer.encrypt(str(admin_id))}" + "\n")

        print(f"User ID <u>{str(uid)}</u> deleted to the list of admins.", True)
        return f"User ID <u>{str(uid)}</u> deleted to the list of admins.", True


file_manager_admins = FileAdminManager()
