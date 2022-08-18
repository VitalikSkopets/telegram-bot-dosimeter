from functools import wraps
from logging import Logger
from typing import Any, Callable, Optional, Sequence

import sentry_sdk
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.logging_config import get_logger

__all__ = ("restricted", "send_action", "debug_handler", "analytics")

from telegram_bot_dosimeter.utils import text_messages

logger = get_logger("default")

ADMIN_ID: int = 413818791
LIST_OF_ADMIN_IDS: Sequence[int] = (413818791,)


def restricted(func: Callable) -> Optional[Callable]:
    """
    Allows you to restrict the access of a handler to only the user_ids specified in
    LIST_OF_ADMINS.
    """

    @wraps(func)
    def wrapped(
        update: Update, context: CallbackContext, *args: Any, **kwargs: Any
    ) -> Optional[Callable]:
        user_id = update.effective_user.id  # type: ignore
        if user_id not in LIST_OF_ADMIN_IDS:
            return None
        return func(update, context, *args, **kwargs)

    return wrapped


def send_action(action: Any) -> Callable:
    """Sends `action` while processing callback handler func command."""

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
    """Send record to Google Analytics 4."""

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


def debug_handler(log_handler: Logger = logger) -> Callable:
    """
    Logs errors raised when executing functions and class methods built into the
    python-telegram-bot library and sends an error message to the admin chat.
    """

    def log_error(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> None:
            try:
                log_handler.debug(f"Callback handler called {func.__name__}")
                return func(*args, **kwargs)
            except Exception as ex:
                update = args[0]
                user = update.message.from_user
                info_message = text_messages.get("info")
                error_message = f"[ADMIN] - [ERROR]: {ex}"

                update.message.reply_text(  # type: ignore
                    f"К сожалению, *{user.first_name}*, {info_message}",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

                if update and hasattr(update, "message"):
                    update.bot.send_message(chat_id=ADMIN_ID, text=error_message)

                log_handler.error(
                    f"In the callback handler {func.__name__} an error occurred {ex}"
                )
                sentry_sdk.capture_exception(error=ex)

        return inner

    return log_error
