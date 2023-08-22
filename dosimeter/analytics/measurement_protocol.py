import requests
from pydantic import BaseModel, ValidationError

from dosimeter.admin import manager
from dosimeter.config import config
from dosimeter.config.logging import CustomAdapter, get_logger
from dosimeter.constants import Action

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
        self.url = config.analytics.uri.geturl()

    def send(self, user_id: int, user_lang_code: str, action: Action) -> None:
        """
        Method for sending a record to Google Analytics 4.
        The Google Analytics Measurement Protocol does not return HTTP error codes,
        even if a Measurement Protocol hit is malformed or missing required parameters.
        """
        payload = self._create_payload(user_id, user_lang_code, action)
        if isinstance(payload, Payload):
            try:
                with requests.session() as session:
                    session.post(self.url, json=payload.dict())
            except Exception as ex:
                logger.exception(
                    "Unable to connect to '%s'. Raised exception: %s"
                    % (config.analytics.uri.hostname, ex),
                    user_id=manager.get_one(user_id),
                )

    @staticmethod
    def _create_payload(uid: int, lang_code: str, action: Action) -> Payload | None:
        """
        A static method for forming the structure and validating
        the payload data values.
        """
        code = (
            lang_code.split("-")[1].upper() if len(lang_code) > 2 else lang_code.upper()
        )
        try:
            param = Param(language=code, engagement_time_msec=str(1))
            event = Event(name=action, params=param)
            payload = Payload(client_id=str(uid), user_id=str(uid), events=[event])
        except ValidationError as ex:
            logger.exception("Validation error. Raised exception: %s" % ex)
            payload = None
        return payload if payload else None
