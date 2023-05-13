import requests

from dosimeter.config import analytics_settings
from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.storage import manager_admins as manager

__all__ = ("Analytics",)


logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class Analytics(object):
    """
    A class that encapsulates the logic of measurements and analytics.
    """

    def __init__(self) -> None:
        """
        Instantiate a Analytics object.
        """
        self.url = analytics_settings.url.geturl()

    def send(self, user_id: int, user_lang_code: str, action: str) -> None:
        """
        Method for sending a record to Google Analytics 4.
        """
        params = {
            "client_id": str(user_id),
            "user_id": str(user_id),
            "events": [
                {
                    "name": action,
                    "params": {
                        "language": user_lang_code,
                        "engagement_time_msec": "1",
                    },
                }
            ],
        }
        try:
            with requests.session() as session:
                session.post(self.url, json=params)
        except Exception as ex:
            logger.exception(
                "Unable to connect to '%s'. Raised exception: %s"
                % (analytics_settings.url.hostname, ex),
                user_id=manager.get_one(user_id),
            )
