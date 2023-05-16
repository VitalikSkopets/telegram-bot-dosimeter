import requests
from pydantic import BaseModel

from dosimeter.config import analytics_settings
from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import Action
from dosimeter.storage import manager_admins as manager

__all__ = (
    "Analytics",
    "Event",
    "Param",
    "Payload",
)


logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class Param(BaseModel):
    """
    Schema for Param.
    """

    language: str
    engagement_time_msec: str = str(1)


class Event(BaseModel):
    """
    Schema for Event.
    """

    name: Action
    params: Param


class Payload(BaseModel):
    """
    Schema for Request.
    """

    client_id: str
    user_id: str
    events: list[Event]


class Analytics(object):
    """
    A class that encapsulates the logic of measurements and analytics.
    """

    def __init__(self) -> None:
        """
        Instantiate a Analytics object.
        """
        self.url = analytics_settings.url.geturl()

    def send(self, user_id: int, user_lang_code: str, action: Action) -> None:
        """
        Method for sending a record to Google Analytics 4.
        The Google Analytics Measurement Protocol does not return HTTP error codes,
        even if a Measurement Protocol hit is malformed or missing required parameters.
        """
        payload = self._create_payload(user_id, user_lang_code, action)

        try:
            with requests.session() as session:
                session.post(self.url, json=payload.dict())
        except Exception as ex:
            logger.exception(
                "Unable to connect to '%s'. Raised exception: %s"
                % (analytics_settings.url.hostname, ex),
                user_id=manager.get_one(user_id),
            )

    @staticmethod
    def _create_payload(uid: int, lang_code: str, action: Action) -> Payload:
        """
        A static method for forming the structure and validating
        the payload data values.
        """
        code = (
            lang_code.split("-")[1].upper() if len(lang_code) > 2 else lang_code.upper()
        )
        param = Param(language=code, engagement_time_msec=str(1))
        event = Event(name=action, params=param)

        return Payload(client_id=str(uid), user_id=str(uid), events=[event])
