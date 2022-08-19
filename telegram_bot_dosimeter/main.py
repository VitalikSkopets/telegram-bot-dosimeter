from typing import Callable, Final

from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.utils.request import Request

from telegram_bot_dosimeter.callback import Callback
from telegram_bot_dosimeter.config import (
    HEROKU_APP_NAME,
    PORT,
    TOKEN,
    WEBHOOK_MODE,
    get_logger,
)
from telegram_bot_dosimeter.constants import (
    Brest_region,
    Gomel_region,
    Grodno_region,
    Minsk_region,
    Mogilev_region,
    Vitebsk_region,
)

__all__ = ("command_handler",)

logger = get_logger(__name__)

# Initial bot application
request = Request(connect_timeout=0.5)
bot = Bot(request=request, token=TOKEN)
updater: Final = Updater(bot=bot, use_context=True)
logger.info(f"Checking bot...\n{updater.bot.get_me()}")

# Initial handlers dispatcher
dispatcher: Final = updater.dispatcher

# Callback class instance
handler = Callback()

# Send my location command handler
send_geolocation_handler = MessageHandler(
    Filters.location,
    handler.send_location_callback,  # type: ignore
)
dispatcher.add_handler(send_geolocation_handler)

# Radiation monitoring command handler
radiation_monitoring_handler = MessageHandler(
    Filters.regex("^(Радиационный мониторинг)$"),
    handler.radiation_monitoring_callback,  # type: ignore
)
dispatcher.add_handler(radiation_monitoring_handler)

# Monitoring points command handler
monitoring_points_handler = MessageHandler(
    Filters.regex("^(Пункты наблюдения)$"),
    handler.monitoring_points_callback,  # type: ignore
)
dispatcher.add_handler(monitoring_points_handler)

# Brest region command handler
brest_region_handler = MessageHandler(
    Filters.regex(f"^({Brest_region.name})$"),
    handler.brest_callback,  # type: ignore
)
dispatcher.add_handler(brest_region_handler)

# Vitebsk region command handler
vitebsk_region_handler = MessageHandler(
    Filters.regex(f"^({Vitebsk_region.name})$"),
    handler.vitebsk_callback,  # type: ignore
)
dispatcher.add_handler(vitebsk_region_handler)

# Gomel region command handler
gomel_region_handler = MessageHandler(
    Filters.regex(f"^({Gomel_region.name})$"),
    handler.gomel_callback,  # type: ignore
)
dispatcher.add_handler(gomel_region_handler)

# Grodno region command handler
grodno_region_handler = MessageHandler(
    Filters.regex(f"^({Grodno_region.name})$"),
    Callback.grodno_callback,  # type: ignore
)
dispatcher.add_handler(grodno_region_handler)

# Minsk region command handler
minsk_region_handler = MessageHandler(
    Filters.regex(f"^({Minsk_region.name})$"),
    handler.minsk_callback,  # type: ignore
)
dispatcher.add_handler(minsk_region_handler)

# Mogilev region command handler
mogilev_region_handler = MessageHandler(
    Filters.regex(f"^({Mogilev_region.name})$"),
    Callback.mogilev_callback,  # type: ignore
)
dispatcher.add_handler(mogilev_region_handler)

# Main menu command handler
main_menu_handler = MessageHandler(
    Filters.regex("^(Главное меню)$"),
    handler.main_menu_callback,  # type: ignore
)
dispatcher.add_handler(main_menu_handler)

# Messages command handler
messages_handler = MessageHandler(
    Filters.text & (~Filters.command),
    handler.messages_callback,  # type: ignore
)
dispatcher.add_handler(messages_handler)


def command_handler(command: str) -> Callable:
    def decorator(callback_handler_func: Callable) -> Callable:
        handler = CommandHandler(command, callback_handler_func)
        dispatcher.add_handler(handler)
        return callback_handler_func

    return decorator


def main() -> None:
    """Application entry point. Bot launch function."""

    if not WEBHOOK_MODE:
        logger.info("Application running in pooling mode...")
        updater.start_polling()
        updater.idle()
        logger.info("Application finished!")
    if HEROKU_APP_NAME and WEBHOOK_MODE:
        logger.info("Application running in webhook mode...")
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
