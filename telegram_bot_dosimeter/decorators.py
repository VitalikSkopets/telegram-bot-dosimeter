from functools import wraps
from typing import Any, Callable, NoReturn, Sequence, Union

from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.logging_config import get_logger

__all__ = ("restricted", "send_action", "log_error", "analytics")

logger = get_logger(__name__)

ADMIN_ID: int = 12345678
LIST_OF_ADMIN_IDS: Sequence[int] = (12345678, 87654321)


def restricted(func: Callable) -> Callable | NoReturn:
    """
    Allows you to restrict the access of a handler to only the user_ids specified in
    LIST_OF_ADMINS.

    :param func: Callable object - handler method.

    :return: Callable object or non-return.
    """

    @wraps(func)
    def wrapped(
        update: Update, context: CallbackContext, *args: Any, **kwargs: Any
    ) -> Union[Callable, None]:
        user_id = update.effective_user.id  # type: ignore
        if user_id not in LIST_OF_ADMIN_IDS:
            return  # type: ignore
        return func(update, context, *args, **kwargs)

    return wrapped


def send_action(action: Any) -> Callable:
    """
    Sends `action` while processing callback handler func command.

    :param action: ChatAction class variables to provide different chat actions.

    :return: Callable object.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def command_func(
            update: Update, context: CallbackContext, *args: Any, **kwargs: Any
        ) -> Callable:
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,  # type: ignore
                action=action,
            )
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


def analytics(func: Callable) -> Callable:
    """
    Send record to Google Analytics 4.

    :param func: Callable object - handler method.

    :return: Callable object - handler method.
    """

    @wraps(func)
    def measurement(*args: Any, **kwargs: Any) -> Callable:
        update = args[0]
        if update and hasattr(update, "message"):
            send_analytics(
                user_id=update.message.chat_id,
                user_lang_code=update.message.from_user.language_code,  # type: ignore
                action_name="Send geolocation",
            )
        return func(*args, **kwargs)

    return measurement


def log_error(func: Callable) -> Callable:
    """
    Logs errors raised when executing functions and class methods built into the
    python-telegram-bot library and sends an error message to the admin

    :param func: Callable object - handler method.

    :return: Callable object - handler method.
    """

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> None:
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            error_message = f"[ADMIN] - [ERROR]: {ex}"
            update = args[0]
            if update and hasattr(update, "message"):
                update.bot.send_message(chat_id=ADMIN_ID, text=error_message)
            logger.error(f"Raised exception {ex}")
            raise ex

    return inner
