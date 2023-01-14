from functools import wraps
from typing import Any, Callable, Optional

import sentry_sdk

from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.config import CustomAdapter, get_logger
from telegram_bot_dosimeter.constants import ADMIN_ID, LIST_OF_ADMIN_IDS, Action
from telegram_bot_dosimeter.messages import Emoji, Message
from telegram_bot_dosimeter.utils import get_uid

__all__ = ("restricted", "send_action", "debug_handler", "analytics")

logger = CustomAdapter(get_logger(__name__), {"user_id": get_uid()})


def restricted(func: Callable) -> Optional[Callable]:
    """
    Allows you to restrict the access of a handler to only the user_ids specified in
    LIST_OF_ADMINS.
    """

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Optional[Callable]:
        update = args[1]
        user = update.effective_user
        if user.id not in LIST_OF_ADMIN_IDS:
            update.effective_message.reply_text("Hey! You are not allowed to use me!")
            logger.warning("Denied unauthorized access", user_id=get_uid(user.id))
            return None
        return func(*args, **kwargs)

    return wrapped


def send_action(action: Any) -> Callable:
    """Sends `action` while processing callback handler func command."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def command_func(*args: Any, **kwargs: Any) -> Callable:
            update = args[1]
            context = args[2]
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,  # type: ignore
                action=action,
            )
            return func(*args, **kwargs)

        return command_func

    return decorator


def analytics(handler_method_name: Action) -> Callable:
    """Send record to Google Analytics 4."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def measurement(*args: Any, **kwargs: Any) -> Callable:
            update = args[1]
            if update and hasattr(update, "message"):
                send_analytics(
                    user_id=update.message.chat_id,
                    user_lang_code=update.message.from_user.language_code,
                    action_name=handler_method_name,
                )
            return func(*args, **kwargs)

        return measurement

    return decorator


def debug_handler(log_handler: CustomAdapter = logger) -> Callable:
    """
    Logs errors raised when executing functions and class methods built into the
    python-telegram-bot library and sends an error message to the admin chat.
    """

    def log_error(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> None:
            update, context = args[1], args[2]
            user = update.effective_user
            try:
                log_handler.debug(
                    "Callback handler '%s' called" % func.__name__,
                    user_id=get_uid(user.id),
                )
                return func(*args, **kwargs)
            except Exception as ex:
                error_msg = f"{Emoji.SOS} [{get_uid(user.id)}] - [ERROR]: {ex}"

                update.message.reply_text(
                    f"К сожалению, <b>{user.first_name}</b>, {Message.INFO}",
                )

                if update and hasattr(update, "message"):
                    context.bot.send_message(chat_id=ADMIN_ID, text=error_msg)

                log_handler.exception(
                    "In the callback handler '%s' an error occurred: %s"
                    % (func.__name__, ex),
                    user_id=get_uid(user.id),
                )
                sentry_sdk.capture_exception(error=ex)

        return inner

    return log_error
