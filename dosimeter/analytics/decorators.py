from functools import wraps
from typing import Any, Callable

from dosimeter.analytics import analytics
from dosimeter.constants import Action


def analytic(action: Action) -> Callable:
    """
    Send record to Google Analytics 4.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def measurement(*args: Any, **kwargs: Any) -> Callable:
            update = args[1]
            if update and hasattr(update, "message"):
                analytics.send(
                    user_id=update.message.chat_id,
                    user_lang_code=update.message.from_user.language_code,
                    action=action,
                )
            return func(*args, **kwargs)

        return measurement

    return decorator
