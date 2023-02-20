import requests

from dosimeter import config
from dosimeter.config import get_logger

__all__ = ("Analytics",)


logger = get_logger(__name__)


class Analytics:
    """A class that encapsulates the logic of measurements and analytics."""

    def __init__(
        self,
        measurement_id: str = config.MEASUREMENT_ID,
        api_secret: str = config.API_SECRET,
    ) -> None:
        """Instantiate a Analytics object"""
        self.measurement_id = measurement_id
        self.api_secret = api_secret
        self.url = (
            f"{config.PROTOKOL}://{config.GOOGLE_DOMEN}/mp/collect?"
            f"measurement_id={self.measurement_id}&api_secret={self.api_secret}"
        )

    def send(self, user_id: int, user_lang_code: str, action: str) -> None:
        """Method for sending a record to Google Analytics 4."""
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
            requests.post(self.url, json=params)
        except Exception as ex:
            logger.exception(
                "Unable to connect to '%s'. Raised exception: %s"
                % (config.GOOGLE_DOMEN, ex)
            )
