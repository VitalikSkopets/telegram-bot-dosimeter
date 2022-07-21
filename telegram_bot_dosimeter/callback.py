from telegram import ChatAction, ParseMode, ReplyKeyboardMarkup, Update, User
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.constants import (
    Brest_region,
    Gomel_region,
    Grodno_region,
    Minsk_region,
    Mogilev_region,
    Vitebsk_region,
)
from telegram_bot_dosimeter.decorators import debug_handler, send_action
from telegram_bot_dosimeter.geolocation import get_nearest_point_location
from telegram_bot_dosimeter.logging_config import get_logger
from telegram_bot_dosimeter.main import command_handler
from telegram_bot_dosimeter.storage.mongodb import MongoDataBase
from telegram_bot_dosimeter.utils import (
    get_avg_radiation_level,
    get_info_about_radiation_monitoring,
    get_info_about_region,
    get_points_with_radiation_level,
    get_user_message,
    greeting,
    main_keyboard,
    text_messages,
)

__all__ = ("Callback",)

logger = get_logger(__name__)

MongoDB = MongoDataBase()


class Callback:
    """A class that encapsulates methods for processing Telegram bot commands."""

    def __init__(self, storage: MongoDataBase = MongoDB) -> None:
        """Constructor method for initializing objects of class Handlers."""
        self.repo = storage
        self.update = Update
        self.context = CallbackContext
        self.user: User = self.update.message.from_user  # type: ignore

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @command_handler("start")
    def start_callback(self) -> None:
        """Start command handler method."""
        start_message = text_messages.get("start")
        self.update.message.reply_text(  # type: ignore
            f"Рад нашему знакомству, *{self.user.first_name}*!{start_message}",
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        self.repo.add_start(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Start command",
        )
        logger.info(f"User {self.user.id} selected Start command")

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @command_handler("help")
    def help_callback(self) -> None:
        """Help command handler method."""
        help_message = text_messages.get("help")
        self.update.message.reply_text(  # type: ignore
            help_message,  # type: ignore
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        self.repo.add_help(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Help command",
        )
        logger.info(f"User {self.user.id} selected Help command")

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def messages_callback(self) -> None:
        """Handler method for an incoming text message from the user."""
        greet_message = text_messages.get("greet")
        unknown_message = text_messages.get("unknown")
        if self.update.message.text.lower() in greeting:  # type: ignore
            self.update.message.reply_text(  # type: ignore
                f"Привет, *{self.user.first_name}*!{greet_message}",
                reply_markup=main_keyboard(),
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            self.repo.add_messages(self.user)
            send_analytics(
                user_id=self.user.id,
                user_lang_code=self.user.language_code,  # type: ignore
                action_name="Greeting message",
            )
            logger.info(f"User {self.user.id} sent a welcome text message")
        else:
            self.update.message.reply_text(  # type: ignore
                unknown_message,  # type: ignore
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            send_analytics(
                user_id=self.user.id,
                user_lang_code=self.user.language_code,  # type: ignore
                action_name="Unknown message",
            )
            logger.info(f"User {self.user.id} sent unknown text message")

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def radiation_monitoring_callback(self) -> None:
        """Handler method for pressing the "Radiation monitoring" button by the user."""
        response = get_info_about_radiation_monitoring()
        mean = get_avg_radiation_level()
        self.update.message.reply_text(  # type: ignore
            f"""
            По состоянию на _{config.TODAY}_ {response}\n\nПо стране
            _среднее_ значение уровня МД гамма-излучения в сети пунктов
            радиационного мониторинга Министерства природных ресурсов и охраны
            окружающей среды Беларусь по состоянию на сегодняшний день составляет
            *{mean:.2f}* мкЗв/ч.
            """,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        self.repo.add_radiation_monitoring(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Radioactive monitoring",
        )
        logger.info(f'User {self.user.id} press button "Radioactive monitoring"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def monitoring_points_callback(self) -> None:
        """Handler method for pressing the "Monitoring points" button by the user."""
        self.update.message.reply_text(  # type: ignore
            "Выбери интересующий регион",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [Brest_region.name],
                    [Vitebsk_region.name],
                    [Gomel_region.name],
                    [Grodno_region.name],
                    [Minsk_region.name],
                    [Mogilev_region.name],
                    ["Главное меню"],
                ],
                resize_keyboard=True,
            ),
        )
        self.repo.add_monitoring_points(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Observation points",
        )
        logger.info(f'User {self.user.id} press button "Observation points"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def brest_callback(self) -> None:
        """Handler method for pressing the "Brest region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Brest_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Brest region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Brest region",
        )
        logger.info(f'User {self.user.id} press button "Brest region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def vitebsk_callback(self) -> None:
        """Handler method for pressing the "Vitebsk region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Vitebsk_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Vitebsk region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Vitebsk region",
        )
        logger.info(f'User {self.user.id} press button "Vitebsk region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def gomel_callback(self) -> None:
        """Handler method for pressing the "Gomel region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Gomel_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Gomel region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Gomel region",
        )
        logger.info(f'User {self.user.id} press button "Gomel region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def grodno_callback(self) -> None:
        """Handler method for pressing the "Grodno region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Grodno_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Grodno region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Grodno region",
        )
        logger.info(f'User {self.user.id} press button "Grodno region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def minsk_callback(self) -> None:
        """Handler method for pressing the "Minsk region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Minsk_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Minsk region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Minsk region",
        )
        logger.info(f'User {self.user.id} press button "Minsk region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def mogilev_callback(self) -> None:
        """Handler method for pressing the "Mogilev region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Mogilev_region.monitoring_points  # type: ignore
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, "Mogilev region")  # type: ignore
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Mogilev region",
        )
        logger.info(f'User {self.user.id} press button "Mogilev region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def main_menu_callback(self) -> None:
        """Handler method for pressing the "Main menu" button by the user."""
        self.update.message.reply_text(  # type: ignore
            f"""
            *{self.user.first_name}*, чтобы узнать по состоянию на _текущую
            дату_ уровень мощности эквивалентной дозы гамма-излучения,
            зафиксированного на _ближайшем_ пункте наблюдения,
            нажми *"Отправить мою геопозицию"*\n\nЧтобы узнать обстановку в
            сети радиационного мониторинга Беларуси, нажми *"Радиационный
            мониторинг"*\n\nЧтобы узнать сводку пунктов наблюдения в сети
            радиационного мониторинга, нажми *"Пункты наблюдения"* и выбери
            интересующий регион
            """,
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Main menu",
        )
        logger.info(f'User {self.user.id} press button "Main menu"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.FIND_LOCATION)
    def send_location_callback(self) -> None:
        """Handler method for pressing the "Send location" button by the user."""
        distance_to_nearest_point, nearest_point_name = get_nearest_point_location(
            latitude=self.update.message.location.latitude,  # type: ignore
            longitude=self.update.message.location.longitude,  # type: ignore
        )

        distance = f"{distance_to_nearest_point:,} м".replace(",", " ")

        for point, value in get_points_with_radiation_level():  # type: ignore
            if nearest_point_name == point:
                self.update.message.reply_text(  # type: ignore
                    f"""
                    _{distance}_ до ближайшего пункта наблюдения
                    "{nearest_point_name}".\n\nВ пункте наблюдения "{point}"
                    по состоянию на _{config.TODAY}_ уровень эквивалентной
                    дозы радиации составляет *{value}* мкЗв/ч.
                    """,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                self.repo.add_location(self.user)
                send_analytics(
                    user_id=self.user.id,
                    user_lang_code=self.user.language_code,  # type: ignore
                    action_name="Send geolocation",
                )
                logger.info(f'User {self.user.id} press button "Send geolocation"')
                break
