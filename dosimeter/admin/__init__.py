from dosimeter.admin.file import FileAdminManager
from dosimeter.admin.interface import AdminManager
from dosimeter.admin.memory import InternalAdminManager

__all__ = (
    "AdminManager",
    "FileAdminManager",
    "InternalAdminManager",
    "file_manager_admins",
    "manager_admins",
)

"""InternalAdminManager class instance"""
manager_admins = InternalAdminManager()

"""FileAdminManager class instance"""
file_manager_admins = FileAdminManager()
