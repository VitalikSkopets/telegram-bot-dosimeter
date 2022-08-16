import requests  # type: ignore

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.logging_config import get_logger

__all__ = ("send_analytics",)

logger = get_logger(__name__)

GOOGLE_DOMEN: str = "www.google-analytics.com"
PROTOKOL: str = "https"
URL: str = (
    f"{PROTOKOL}://{GOOGLE_DOMEN}/mp/collect?"
    f"measurement_id={config.MEASUREMENT_ID}&api_secret={config.API_SECRET}"
)


def send_analytics(user_id: int, user_lang_code: str, action_name: str) -> None:
    """Send record to Google Analytics 4."""
    params = {
        "client_id": str(user_id),
        "user_id": str(user_id),
        "events": [
            {
                "name": action_name,
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
        logger.error(
            f"Unable to connect to '{GOOGLE_DOMEN}'. Raised exception: {ex}",
            exc_info=True,
        )
