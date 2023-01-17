from dosimeter.constants import ADMIN_ID, LIST_OF_ADMIN_IDS

__all__ = ("InternalAdminManager", "manager_admins")


class InternalAdminManager:
    LIST_OF_ADMINS: tuple[int, int] = LIST_OF_ADMIN_IDS

    def __init__(self) -> None:
        """Constructor method for initializing objects of class InternalManageAdmin."""
        self.temp_list_admins = [*self.LIST_OF_ADMINS]

    def get_one(self, uid: str | int | None = None) -> str | int | None:
        if uid and int(uid) not in self.LIST_OF_ADMINS:
            return int(uid)
        if uid and int(uid) in self.LIST_OF_ADMINS:
            return "ADMIN"
        return None

    def get_all(self) -> str:
        if not self.temp_list_admins:
            return "Admins not assigned"
        output = []
        for num, admin_id in enumerate(self.temp_list_admins, 1):
            message = "{}: {} - Main admin" if admin_id == ADMIN_ID else "{}: {}"
            output.append(message.format(num, admin_id))
        return "\n".join(output)

    def add(self, uid: int) -> tuple[str, bool]:
        if uid in self.temp_list_admins:
            return "The user ID has already been added to the list of admins.", False
        self.temp_list_admins.append(uid)
        return f"User ID <u>{uid}</u> added to the list of admins.", True

    def delete(self, uid: int) -> tuple[str, bool]:
        if uid not in self.temp_list_admins:
            return "This user ID is not in the list of administrators.", False
        self.temp_list_admins.remove(uid)
        return f"User ID <u>{uid}</u> deleted to the list of admins.", True


manager_admins = InternalAdminManager()
