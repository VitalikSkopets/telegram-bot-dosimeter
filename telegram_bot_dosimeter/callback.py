from telegram import ChatAction, ParseMode, ReplyKeyboardMarkup, Update, User
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.config import get_logger
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

mongo_atlas__repo = MongoDataBase()


class Callback:
    """A class that encapsulates methods for processing Telegram bot commands."""

    def __init__(self, repo: MongoDataBase = mongo_atlas__repo) -> None:
        """Constructor method for initializing objects of class Handlers."""
        self.repo = repo
        self.update = Update
        self.context = CallbackContext
        self.user: User = self.update.message.from_user  # type: ignore
        self.logger = get_logger("%s.%s" % (__name__, self.__class__.__qualname__))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @command_handler("start")
    def start_callback(self) -> None:
        """Start command handler method."""
        start_message = text_messages["start"]
        self.update.message.reply_text(  # type: ignore
            f"Рад нашему знакомству, *{self.user.first_name}*!{start_message}",
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        self.repo.add_start(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.START,
        )
        self.logger.info("User %d selected '%s'" % (self.user.id, Action.START))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @command_handler("help")
    def help_callback(self) -> None:
        """Help command handler method."""
        help_message = text_messages["help"]
        self.update.message.reply_text(  # type: ignore
            help_message,
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        self.repo.add_help(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.HELP,
        )
        self.logger.info("User %d selected '%s'" % (self.user.id, Action.HELP))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def messages_callback(self) -> None:
        """Handler method for an incoming text message from the user."""
        greet_message = text_messages["greet"]
        unknown_message = text_messages["unknown"]
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
                action_name=Action.GREETING,
            )
            self.logger.info("User %d sent a welcome text message" % self.user.id)
        else:
            self.update.message.reply_text(  # type: ignore
                unknown_message,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            send_analytics(
                user_id=self.user.id,
                user_lang_code=self.user.language_code,  # type: ignore
                action_name=Action.MESSAGE,
            )
            self.logger.info("User %d sent unknown text message" % self.user.id)

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
            action_name=Action.MONITORING,
        )
        self.logger.info(
            "User %d press button '%s'" % (self.user.id, Action.MONITORING)
        )

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def monitoring_points_callback(self) -> None:
        """Handler method for pressing the "Monitoring points" button by the user."""
        self.update.message.reply_text(  # type: ignore
            "Выбери интересующий регион",
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
        self.repo.add_monitoring_points(self.user)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.POINTS,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.POINTS))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def brest_callback(self) -> None:
        """Handler method for pressing the "Brest region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Brest_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.BREST)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.BREST,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.BREST))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def vitebsk_callback(self) -> None:
        """Handler method for pressing the "Vitebsk region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Vitebsk_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.VITEBSK)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.VITEBSK,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.VITEBSK))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def gomel_callback(self) -> None:
        """Handler method for pressing the "Gomel region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Gomel_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.GOMEL)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.GOMEL,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.GOMEL))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def grodno_callback(self) -> None:
        """Handler method for pressing the "Grodno region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Grodno_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.GRODNO)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.GRODNO,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.GRODNO))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def minsk_callback(self) -> None:
        """Handler method for pressing the "Minsk region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Minsk_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.MINSK)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.MINSK,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.MINSK))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def mogilev_callback(self) -> None:
        """Handler method for pressing the "Mogilev region" button by the user."""
        table, values_by_region = get_info_about_region(
            region=Mogilev_region.monitoring_points
        )

        self.update.message.reply_text(  # type: ignore
            get_user_message(table, values_by_region),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        self.repo.add_region(self.user, Action.MOGILEV)
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name=Action.MOGILEV,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.MOGILEV))

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
            action_name=Action.MAIN_MENU,
        )
        self.logger.info("User %d press button '%s'" % (self.user.id, Action.MAIN_MENU))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.FIND_LOCATION)
    def send_location_callback(self) -> None:
        """Handler method for pressing the "Send location" button by the user."""
        distance_to_nearest_point, nearest_point_name = get_nearest_point_location(
            latitude=self.update.message.location.latitude,  # type: ignore
            longitude=self.update.message.location.longitude,  # type: ignore
        )

        distance = f"{distance_to_nearest_point:,} м".replace(",", " ")

        for point, value in get_points_with_radiation_level():
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
                    action_name=Action.LOCATION,
                )
                self.logger.info(
                    "User %d press button '%s'" % (self.user.id, Action.LOCATION)
                )
                break
