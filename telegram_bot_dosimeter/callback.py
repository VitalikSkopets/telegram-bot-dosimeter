# type: ignore
from telegram import ChatAction, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.config import CustomAdapter, get_logger
from telegram_bot_dosimeter.constants import (
    BREST,
    GOMEL,
    GRODNO,
    LIST_ADMIN_IDS,
    MAIN_MENU,
    MINSK,
    MOGILEV,
    MONITORING,
    NEXT,
    NEXT_ARROW,
    POINTS,
    PREV,
    PREV_ARROW,
    TOTAL_COUNT_USERS,
    VITEBSK,
    Action,
    Brest_region,
    Button,
    Gomel_region,
    Grodno_region,
    Minsk_region,
    Mogilev_region,
    MonitoringPoint,
    Vitebsk_region,
)
from telegram_bot_dosimeter.decorators import debug_handler, restricted, send_action
from telegram_bot_dosimeter.geolocation import get_nearest_point_location
from telegram_bot_dosimeter.keyboards import (
    admin_keyboard,
    main_keyboard,
    points_keyboard,
)
from telegram_bot_dosimeter.messages import Message
from telegram_bot_dosimeter.storage.mongodb import MongoDataBase
from telegram_bot_dosimeter.utils import (
    get_admin_ids,
    get_avg_radiation_level,
    get_info_about_radiation_monitoring,
    get_info_about_region,
    get_points_with_radiation_level,
    get_uid,
    get_user_message,
    greeting,
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
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Рад нашему знакомству, <b>{}</b>!{}".format(
                user.first_name, Message.START
            ),
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
            text=Message.HELP,
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
            case MONITORING.name:
                return self.radiation_monitoring_callback(update, context)
            case POINTS.name:
                button_list = (
                    BREST,
                    VITEBSK,
                    MAIN_MENU,
                    NEXT,
                )
                return self.monitoring_points_callback(update, context, button_list)
            case NEXT.name:
                button_list = (
                    GOMEL,
                    GRODNO,
                    PREV_ARROW,
                    NEXT_ARROW,
                )
                keyboard = points_keyboard(button_list)
                action = Action.NEXT
                return self.pagination_callback(update, context, keyboard, action)
            case NEXT_ARROW.name:
                button_list = (
                    MINSK,
                    MOGILEV,
                    PREV,
                    MAIN_MENU,
                )
                keyboard = points_keyboard(button_list)
                action = Action.NEXT
                return self.pagination_callback(update, context, keyboard, action)
            case PREV.name:
                button_list = (
                    GOMEL,
                    GRODNO,
                    PREV_ARROW,
                    NEXT_ARROW,
                )
                keyboard = points_keyboard(button_list)
                action = Action.PREV
                return self.pagination_callback(update, context, keyboard, action)
            case PREV_ARROW.name:
                button_list = (
                    BREST,
                    VITEBSK,
                    MAIN_MENU,
                    NEXT,
                )
                keyboard = points_keyboard(button_list)
                action = Action.PREV
                return self.pagination_callback(update, context, keyboard, action)
            case MAIN_MENU.name:
                return self.main_menu_callback(update, context)
            case BREST.name:
                points = Brest_region.monitoring_points
                action = Action.BREST
            case VITEBSK.name:
                points = Vitebsk_region.monitoring_points
                action = Action.VITEBSK
            case GOMEL.name:
                points = Gomel_region.monitoring_points
                action = Action.GOMEL
            case GRODNO.name:
                points = Grodno_region.monitoring_points
                action = Action.GRODNO
            case MINSK.name:
                points = Minsk_region.monitoring_points
                action = Action.MINSK
            case MOGILEV.name:
                points = Mogilev_region.monitoring_points
                action = Action.MOGILEV
            case _:
                return self.greeting_callback(update, context)

        return self.points_callback(update, context, points, action)

    def pagination_callback(
        self,
        update: Update,
        context: CallbackContext,
        keyboard: ReplyKeyboardMarkup,
        action: Action,
    ) -> None:
        """
        Handler method for pressing the "Next" or "Prev" keyboard button by the user.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=Message.REGION,
            reply_markup=keyboard,
        )
        logger.info(self.LOG_MSG % action.value, user_id=get_uid(user.id))

    def greeting_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for an incoming text message from the user."""
        user = update.effective_user
        message = update.message.text
        greet_msg = Message.GREET
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
                text=Message.UNKNOWN,
            )
            send_analytics(
                user_id=user.id,
                user_lang_code=user.language_code,
                action_name=Action.MESSAGE,
            )
            logger.info("User sent unknown text message", user_id=get_uid(user.id))

    def radiation_monitoring_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Handler method for pressing the "Radiation monitoring" button by the user."""
        user = update.effective_user
        response = get_info_about_radiation_monitoring()
        mean = get_avg_radiation_level()
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=Message.RADIATION.format(config.TODAY, response, mean),
        )
        self.repo.add_radiation_monitoring(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.MONITORING,
        )
        logger.info(self.LOG_MSG % Action.MONITORING.value, user_id=get_uid(user.id))

    def monitoring_points_callback(
        self, update: Update, context: CallbackContext, button_list: tuple[Button, ...]
    ) -> None:
        """Handler method for pressing the "Monitoring points" button by the user."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=Message.REGION,
            reply_markup=points_keyboard(button_list),
        )
        self.repo.add_monitoring_points(user)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=Action.POINTS,
        )
        logger.info(self.LOG_MSG % Action.POINTS.value, user_id=get_uid(user.id))

    def points_callback(
        self,
        update: Update,
        context: CallbackContext,
        points: tuple[MonitoringPoint, ...],
        action: Action,
    ) -> None:
        """Handler method for pressing the "* region" button by the user."""
        user = update.effective_user
        table, values_by_region = get_info_about_region(region=points)

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_user_message(table, values_by_region),
        )

        self.repo.add_region(user, action)
        send_analytics(
            user_id=user.id,
            user_lang_code=user.language_code,
            action_name=action,
        )
        logger.info(self.LOG_MSG % action.value, user_id=get_uid(user.id))

    def main_menu_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for pressing the "Main menu" button by the user."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=f"<b>{user.first_name}</b>, чтобы узнать {Message.DESCRIPTION}",
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
                    text=Message.LOCATION.format(
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

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @restricted
    def admin_callback(self, update: Update, context: CallbackContext) -> None:
        """Admin command handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=Message.ADMIN,
            reply_markup=admin_keyboard(),
        )
        logger.debug(self.LOG_MSG % Action.ADMIN.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def get_count_users_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Get total count users admin command handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.repo.get_users_count(user),
            reply_markup=main_keyboard(),
        )
        logger.debug(self.LOG_MSG % Action.GET_COUNT.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def get_list_admin_ids_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Get a list of admin IDs admin command handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_admin_ids(),
            reply_markup=main_keyboard(),
        )
        logger.debug(self.LOG_MSG % Action.GET_LIST.value, user_id=get_uid(user.id))

    @debug_handler(log_handler=logger)
    def keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """Inline keyboard buttons handler"""
        query = update.callback_query
        match query.data:
            case TOTAL_COUNT_USERS.callback_data:
                return self.get_count_users_callback(update, context)
            case LIST_ADMIN_IDS.callback_data:
                return self.get_list_admin_ids_callback(update, context)
