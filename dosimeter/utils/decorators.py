from functools import wraps
from typing import Any, Callable, Optional

import sentry_sdk

from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import ADMIN_ID, LIST_OF_ADMIN_IDS
from dosimeter.storage import manager_admins as manager
from dosimeter.template_engine import message_engine
from dosimeter.template_engine.engine import Template

__all__ = (
    "debug_handler",
    "restricted",
    "send_action",
)


logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


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
            logger.warning(
                "Denied unauthorized access", user_id=manager.get_one(user.id)
            )
            return None
        return func(*args, **kwargs)

    return wrapped


def send_action(action: Any) -> Callable:
    """
    Sends `action` while processing callback handler func command.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def command_func(*args: Any, **kwargs: Any) -> Callable:
            update = args[1]
            context = args[2]
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=action,
            )
            return func(*args, **kwargs)

        return command_func

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
                    user_id=manager.get_one(user.id),
                )
                return func(*args, **kwargs)
            except Exception as ex:
                update.message.reply_text(
                    message_engine.render(
                        Template.USER_ERROR,
                        user=user,
                    ),
                )

                if update and hasattr(update, "message"):
                    context.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=message_engine.render(
                            Template.ADMIN_ERROR,
                            admin=manager.get_one(user.id),
                            func_name=func.__name__,
                            exc_info=ex,
                        ),
                    )

                log_handler.exception(
                    "In the callback handler '%s' an error occurred: %s"
                    % (func.__name__, ex),
                    user_id=manager.get_one(user.id),
                )
                sentry_sdk.capture_exception(error=ex)

        return inner

    return log_error
