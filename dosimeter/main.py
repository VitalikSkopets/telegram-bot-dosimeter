import pytz
from telegram import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Defaults,
    ExtBot,
    Filters,
    MessageHandler,
    Updater,
)
from telegram.utils.request import Request

from dosimeter import config
from dosimeter.callback import Callback, handler  # type: ignore[attr-defined]
from dosimeter.constants import Command

logger = config.get_logger(__name__)


class DosimeterBot:
    """The wrapper class encapsulates the logic of initializing and launching
    the DosimeterBot object"""

    TOKEN = config.TOKEN
    WEBHOOK_MODE = config.WEBHOOK_MODE
    HEROKU_APP = config.HEROKU_APP
    PORT = config.PORT

    def __init__(self, callback: Callback = handler) -> None:
        """Instantiate a DosimeterBot object"""

        # Initial and check bot application
        defaults = Defaults(
            parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Minsk")
        )
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = ExtBot(request=request, token=self.TOKEN, defaults=defaults)
        self.updater = Updater(bot=bot, use_context=True)
        logger.info(f"Checking bot...{self.updater.bot.get_me()}")
        self.handler = callback

        # Start command handler
        start_handler = CommandHandler(
            Command.START,
            self.handler.start_callback,
        )
        self.updater.dispatcher.add_handler(start_handler)

        # Help command handler
        help_handler = CommandHandler(
            Command.HELP,
            self.handler.help_callback,
        )
        self.updater.dispatcher.add_handler(help_handler)

        # Admin command handler
        admin_handler = CommandHandler(
            Command.ADMIN,
            self.handler.admin_callback,
        )
        self.updater.dispatcher.add_handler(admin_handler)

        # Send my location command handler
        send_geolocation_handler = MessageHandler(
            Filters.location,
            self.handler.send_location_callback,
        )
        self.updater.dispatcher.add_handler(send_geolocation_handler)

        # Messages command handler
        message_handler = MessageHandler(
            Filters.text & (~Filters.command),
            self.handler.message_callback,
        )
        self.updater.dispatcher.add_handler(message_handler)

        # Inline keyboard button handler
        button_handler = CallbackQueryHandler(
            callback=self.handler.keyboard_callback,
            pass_chat_data=True,
        )
        self.updater.dispatcher.add_handler(button_handler)

    def start(self) -> None:
        """Method for launching the DosimeterBot object"""
        if not self.WEBHOOK_MODE:
            logger.info("Application running in pooling mode...")
            # Start the Bot
            self.updater.start_polling()
            self.updater.idle()
            logger.info("Application finished!")
        if self.HEROKU_APP and self.WEBHOOK_MODE:
            logger.info("Application running in webhook mode...")
            # Start the Bot
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=self.PORT,
                url_path=self.TOKEN,
                webhook_url=f"https://{self.HEROKU_APP}.herokuapp.com/{self.TOKEN}",
            )
            self.updater.idle()
            logger.info("Application finished!")


if __name__ == "__main__":
    bot_instance = DosimeterBot()
    bot_instance.start()
