import requests

from dosimeter import config
from dosimeter.config import get_logger

__all__ = ("send_analytics",)


logger = get_logger(__name__)

URL: str = (
    f"{config.PROTOKOL}://{config.GOOGLE_DOMEN}/mp/collect?"
    f"measurement_id={config.MEASUREMENT_ID}&api_secret={config.API_SECRET}"
)


def send_analytics(user_id: int, user_lang_code: str, action: str) -> None:
    """Send record to Google Analytics 4."""
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
        requests.post(URL, json=params)
    except Exception as ex:
        logger.exception(
            "Unable to connect to '%s'. Raised exception: %s"
            % (config.GOOGLE_DOMEN, ex)
        )
