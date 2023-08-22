from dosimeter.admin.file import FileAdminManager
from dosimeter.admin.interface import AdminManager
from dosimeter.admin.memory import InternalAdminManager

__all__ = (
    "AdminManager",
    "FileAdminManager",
    "InternalAdminManager",
    "manager",
)

"""InternalAdminManager class instance"""
manager = InternalAdminManager()
