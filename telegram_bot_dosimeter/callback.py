# type: ignore
from telegram import ChatAction, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.config import CustomAdapter, get_logger
from telegram_bot_dosimeter.constants import (
    Action,
    Brest_region,
    Button,
    Gomel_region,
    Grodno_region,
    Minsk_region,
    Mogilev_region,
    Vitebsk_region,
)
from telegram_bot_dosimeter.decorators import debug_handler, send_action
from telegram_bot_dosimeter.geolocation import get_nearest_point_location
from telegram_bot_dosimeter.storage.mongodb import MongoDataBase
from telegram_bot_dosimeter.utils import (
    arrow,
    get_avg_radiation_level,
    get_info_about_radiation_monitoring,
    get_info_about_region,
    get_points_with_radiation_level,
    get_uid,
    get_user_message,
    greeting,
    main_keyboard,
    text_messages,
)

__all__ = ("Callback",)

logger = CustomAdapter(get_logger(__name__), {"user_id": get_uid()})

mongo_atlas__repo = MongoDataBase()


class Callback:
    """A class that encapsulates methods for processing Telegram bot commands."""

    LOG_MSG = "User selected '%s'"

    def __init__(self, repo: MongoDataBase = mongo_atlas__repo) -> None:
        """Constructor method for initializing objects of class Handlers."""
        self.repo = repo

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def start_callback(self, update: Update, context: CallbackContext) -> None:
        """Start command handler method."""
        user = update.effective_user
        msg = text_messages["start"]
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Рад нашему знакомству, <b>{}</b>!{}".format(user.first_name, msg),
            reply_markup=main_keyboard(),
        )
        self.repo.add_start(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.START,
        )
        logger.info(self.LOG_MSG % Action.START.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def help_callback(self, update: Update, context: CallbackContext) -> None:
        """Help command handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=text_messages["help"],
            reply_markup=main_keyboard(),
        )
        self.repo.add_help(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.HELP,
        )
        logger.info(self.LOG_MSG % Action.HELP.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def message_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for an incoming text messages from the user."""
        match update.message.text:
            case Brest_region.name:
                return self.brest_callback(update, context)
            case Vitebsk_region.name:
                return self.vitebsk_callback(update, context)
            case Gomel_region.name:
                return self.gomel_callback(update, context)
            case Grodno_region.name:
                return self.grodno_callback(update, context)
            case Minsk_region.name:
                return self.minsk_callback(update, context)
            case Mogilev_region.name:
                return self.mogilev_callback(update, context)
            case _:
                return self.greeting_callback(update, context)

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def greeting_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for an incoming text message from the user."""
        user = update.effective_user
        message = update.message.text
        greet_msg = text_messages["greet"]
        if message and message.lower() in greeting:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text="Привет, <b>{}</b>!{}".format(user.first_name, greet_msg),
                reply_markup=main_keyboard(),
            )
            self.repo.add_messages(user)
            send_analytics(
                user_id=user.id,
                user_lang_code=user.language_code,
                action_name=Action.GREETING,
            )
            logger.info("User sent a welcome text message", user_id=get_uid(user.id))
        else:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=text_messages["unknown"],
            )
            send_analytics(
                user_id=user.id,
                user_lang_code=user.language_code,
                action_name=Action.MESSAGE,
            )
            logger.info("User sent unknown text message", user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def radiation_monitoring_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Handler method for pressing the "Radiation monitoring" button by the user."""
        user = update.effective_user
        response = get_info_about_radiation_monitoring()
        mean = get_avg_radiation_level()
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Сегодня <i>{}</i> {}\n\nПо стране <i>среднее</i> значение "
            "уровня МД гамма-излучения в сети пунктов радиационного мониторинга "
            "Министерства природных ресурсов и охраны окружающей среды Беларусь "
            "по состоянию на сегодняшний день составляет <b>{:.2f}</b> "
            "мкЗв/ч.".format(config.TODAY, response, mean),
        )
        self.repo.add_radiation_monitoring(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.MONITORING,
        )
        logger.info(self.LOG_MSG % Action.MONITORING.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def monitoring_points_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Handler method for pressing the "Monitoring points" button by the user."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Выбери интересующий регион {}".format(arrow),
            reply_markup=ReplyKeyboardMarkup(
                [
                    [Button.BREST],
                    [Button.VITEBSK],
                    [Button.GOMEL],
                    [Button.GRODNO],
                    [Button.MINSK],
                    [Button.MOGILEV],
                    [Button.MAIN_MENU],
                ],
                resize_keyboard=True,
            ),
        )
        self.repo.add_monitoring_points(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.POINTS,
        )
        logger.info(self.LOG_MSG % Action.POINTS.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def brest_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Brest region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Brest_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.BREST)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.BREST,
        )
        logger.info(self.LOG_MSG % Action.BREST.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def vitebsk_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Vitebsk region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Vitebsk_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.VITEBSK)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.VITEBSK,
        )
        logger.info(self.LOG_MSG % Action.VITEBSK.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def gomel_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Gomel region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Gomel_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.GOMEL)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.GOMEL,
        )
        logger.info(self.LOG_MSG % Action.GOMEL.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def grodno_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Grodno region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Grodno_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.GRODNO)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.GRODNO,
        )
        logger.info(self.LOG_MSG % Action.GRODNO.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def minsk_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Minsk region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Minsk_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.MINSK)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.MINSK,
        )
        logger.info(self.LOG_MSG % Action.MINSK.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def mogilev_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Mogilev region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(
            region=Mogilev_region.monitoring_points
        )

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, Action.MOGILEV)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.MOGILEV,
        )
        logger.info(self.LOG_MSG % Action.MOGILEV.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def main_menu_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Main menu" button by the user."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=text_messages["desc"].format(user.first_name),
            reply_markup=main_keyboard(),
        )
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.MAIN_MENU,
        )
        logger.info(self.LOG_MSG % Action.MAIN_MENU.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.FIND_LOCATION)
    def send_location_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Send location" button by the user."""
        user = update.effective_user
        distance_to_nearest_point, nearest_point_name = get_nearest_point_location(
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
        )

        distance = f"{distance_to_nearest_point:,} м".replace(",", " ")

        for point, value in get_points_with_radiation_level():
            if nearest_point_name == point:
                context.bot.send_message(
                    chat_id=update.effective_message.chat_id,
                    text=text_messages["location"].format(
                        distance,
                        nearest_point_name,
                        point,
                        config.TODAY,
                        value,
                    ),
                )
                self.repo.add_location(user)
                send_analytics(
                    user_id=user.id,
                    user_lang_code=user.language_code,
                    action_name=Action.LOCATION,
                )
                logger.info(
                    self.LOG_MSG % Action.LOCATION.value, user_id=get_uid(user.id)
                )
                break
