from dosimeter.storage.mongo import CloudMongoDataBase
from dosimeter.storage.repository import Repository

__all__ = (
    "CloudMongoDataBase",
    "Repository",
    "mongo_cloud",
)

"""CloudMongoDataBase class instance"""
mongo_cloud = CloudMongoDataBase()
