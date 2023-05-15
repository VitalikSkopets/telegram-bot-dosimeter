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
    "Request",
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


class Request(BaseModel):
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
        """
        param = Param(language=user_lang_code, engagement_time_msec=str(1))
        event = Event(name=action, params=param)
        request = Request(client_id=str(user_id), user_id=str(user_id), events=[event])

        try:
            with requests.session() as session:
                session.post(self.url, json=request.dict())
        except Exception as ex:
            logger.exception(
                "Unable to connect to '%s'. Raised exception: %s"
                % (analytics_settings.url.hostname, ex),
                user_id=manager.get_one(user_id),
            )
