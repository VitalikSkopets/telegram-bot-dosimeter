import sys
from urllib.parse import urljoin

import pytz
from telegram import ParseMode, ext
from telegram.utils.request import Request

from dosimeter.config import config
from dosimeter.config.logging import get_logger
from dosimeter.constants import Command
from dosimeter.handler import MessageHandler  # type: ignore[attr-defined]

logger = get_logger(__name__)


class DosimeterBot(object):
    """
    The wrapper class encapsulates the logic of initializing and launching
    the DosimeterBot object.
    """

    def __init__(self, token: str, callback: MessageHandler = MessageHandler()) -> None:
        """
        Instantiate a DosimeterBot object.
        """
        self.token = token
        self.handler = callback

        # Initial bot application
        defaults = ext.Defaults(
            parse_mode=ParseMode.HTML, tzinfo=pytz.timezone(config.app.timezone)
        )
        request = Request(con_pool_size=8, connect_timeout=0.5, read_timeout=1.0)
        bot = ext.ExtBot(request=request, token=self.token, defaults=defaults)
        self.updater = ext.Updater(bot=bot, use_context=True)

        dispatcher = self.updater.dispatcher  # type: ignore[has-type,unused-ignore]

        command_handlers = {
            Command.START: self.handler.start_callback,
            Command.HELP: self.handler.help_callback,
            Command.DONATE: self.handler.donate_callback,
            Command.ADMIN: self.handler.admin_callback,
        }

        for command_name, command_handler in command_handlers.items():
            dispatcher.add_handler(ext.CommandHandler(command_name, command_handler))

        message_handlers = {
            ext.Filters.location: self.handler.send_location_callback,
            ext.Filters.text & (~ext.Filters.command): self.handler.message_callback,
        }

        for message_name, message_handler in message_handlers.items():
            dispatcher.add_handler(ext.MessageHandler(message_name, message_handler))

        # Inline keyboard button handler
        button_handler = ext.CallbackQueryHandler(
            callback=self.handler.keyboard_callback,
            pass_chat_data=True,
        )
        dispatcher.add_handler(button_handler)

    @property
    def is_checked(self) -> bool:
        """
        Method for testing your bots auth token. Requires no parameters.
        Returns basic information about the bot in form of a User object.
        """
        info = self.updater.bot.get_me()  # type: ignore[has-type,unused-ignore]
        if not info or info.username != self.__class__.__name__:
            return False
        logger.info("Checking bot... %s ...successful!", info)
        return True

    def start(self) -> None:
        """
        Method for launching the DosimeterBot object.
        """
        if not config.app.webhook_mode:
            logger.info("Application running in pooling mode...")
            # Start the Bot
            self.updater.start_polling()
            self.updater.idle()
            logger.info("Application finished!")
        if config.app.webhook_mode and config.heroku.app:
            logger.info("Application running in webhook mode...")
            # Start the Bot
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=config.heroku.port,
                url_path=self.token,
                webhook_url=urljoin(config.heroku.webhook_uri, self.token),
            )
            self.updater.idle()
            logger.info("Application finished!")


def main() -> None:
    """
    Application entry point.
    """
    instance_of_bot = DosimeterBot(config.app.token)
    if not instance_of_bot.is_checked:
        return None
    instance_of_bot.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as exc:
        logger.exception("Raised exception: %s", exc)
        sys.exit(1)
