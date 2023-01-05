from typing import Final

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

from telegram_bot_dosimeter.callback import Callback  # type: ignore
from telegram_bot_dosimeter.config import (
    HEROKU_APP_NAME,
    PORT,
    TOKEN,
    WEBHOOK_MODE,
    get_logger,
)
from telegram_bot_dosimeter.constants import Button, Command

logger = get_logger(__name__)


def main() -> None:
    """Application entry point. Bot launch function."""

    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Minsk"))

    """Initial and check bot application"""
    request = Request(connect_timeout=0.5, read_timeout=1.0)
    bot = ExtBot(request=request, token=TOKEN, defaults=defaults)
    updater: Final = Updater(bot=bot, use_context=True)
    logger.info(f"Checking bot...{updater.bot.get_me()}")

    """Get the dispatcher to register handlers"""
    dispatcher: Final = updater.dispatcher

    """Callback class instance"""
    handler = Callback()

    # Start command handler
    start_handler = CommandHandler(
        Command.START,
        handler.start_callback,  # type: ignore
    )
    dispatcher.add_handler(start_handler)

    # Help command handler
    help_handler = CommandHandler(
        Command.HELP,
        handler.help_callback,  # type: ignore
    )
    dispatcher.add_handler(help_handler)

    # Admin command handler
    admin_handler = CommandHandler(
        Command.ADMIN,
        handler.admin_callback,  # type: ignore
    )
    dispatcher.add_handler(admin_handler)

    # Send my location command handler
    send_geolocation_handler = MessageHandler(
        Filters.location,
        handler.send_location_callback,  # type: ignore
    )
    dispatcher.add_handler(send_geolocation_handler)

    # Radiation monitoring command handler
    radiation_monitoring_handler = MessageHandler(
        Filters.regex(f"^({Button.MONITORING})$"),
        handler.radiation_monitoring_callback,  # type: ignore
    )
    dispatcher.add_handler(radiation_monitoring_handler)

    # Monitoring points command handler
    monitoring_points_handler = MessageHandler(
        Filters.regex(f"^({Button.POINTS})$"),
        handler.monitoring_points_callback,  # type: ignore
    )
    dispatcher.add_handler(monitoring_points_handler)

    # Main menu command handler
    main_menu_handler = MessageHandler(
        Filters.regex(f"^({Button.MAIN_MENU})$"),
        handler.main_menu_callback,  # type: ignore
    )
    dispatcher.add_handler(main_menu_handler)

    # Messages command handler
    message_handler = MessageHandler(
        Filters.text & (~Filters.command),
        handler.message_callback,  # type: ignore
    )
    dispatcher.add_handler(message_handler)

    # Inline keyboard button handler
    button_handler = CallbackQueryHandler(
        callback=handler.keyboard_callback,
        pass_chat_data=True,
    )
    dispatcher.add_handler(button_handler)

    if not WEBHOOK_MODE:
        logger.info("Application running in pooling mode...")
        # Start the Bot
        updater.start_polling()
        updater.idle()
        logger.info("Application finished!")
    if HEROKU_APP_NAME and WEBHOOK_MODE:
        logger.info("Application running in webhook mode...")
        # Start the Bot
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}",
        )
        updater.idle()
        logger.info("Application finished!")


if __name__ == "__main__":
    main()
