import pytz
from telegram import ParseMode, ext
from telegram.utils.request import Request

from dosimeter.config import settings
from dosimeter.config.logger import get_logger
from dosimeter.constants import Command
from dosimeter.handle import Handler, handler

logger = get_logger(__name__)


class DosimeterBot(object):
    """
    The wrapper class encapsulates the logic of initializing and launching
    the DosimeterBot object.
    """

    WEBHOOK_MODE: bool = settings.WEBHOOK_MODE
    HEROKU_APP: str = settings.HEROKU_APP
    PORT: int = settings.PORT

    def __init__(self, token: str, callback: Handler = handler) -> None:
        """
        Instantiate a DosimeterBot object.
        """
        self.token = token

        # Initial and check bot application
        defaults = ext.Defaults(
            parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Minsk")
        )
        request = Request(con_pool_size=8, connect_timeout=0.5, read_timeout=1.0)
        bot = ext.ExtBot(request=request, token=self.token, defaults=defaults)
        self.updater = ext.Updater(bot=bot, use_context=True)
        logger.info(f"Checking bot...{self.updater.bot.get_me()}")
        self.handler = callback
        dispatcher = self.updater.dispatcher

        command_handlers = {
            Command.START: self.handler.start_callback,
            Command.HELP: self.handler.help_callback,
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

    def start(self) -> None:
        """
        Method for launching the DosimeterBot object.
        """
        if not self.WEBHOOK_MODE:
            logger.info("Application running in pooling mode...")
            # Start the Bot
            self.updater.start_polling()
            self.updater.idle()
            logger.info("Application finished!")
        if self.WEBHOOK_MODE and self.HEROKU_APP:
            logger.info("Application running in webhook mode...")
            # Start the Bot
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=self.PORT,
                url_path=self.token,
                webhook_url=f"https://{self.HEROKU_APP}.herokuapp.com/{self.token}",
            )
            self.updater.idle()
            logger.info("Application finished!")


def main() -> None:
    """
    Application entry point.
    """
    instance_of_bot = DosimeterBot(settings.TOKEN)
    instance_of_bot.start()


if __name__ == "__main__":
    bot_instance = DosimeterBot(settings.TOKEN)
    bot_instance.start()
