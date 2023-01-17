# type: ignore
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.config import CustomAdapter, get_logger
from telegram_bot_dosimeter.constants import (
    Action,
    Brest_region,
    Buttons,
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
from telegram_bot_dosimeter.storage.mongodb import MongoDataBase, mongo_atlas__repo
from telegram_bot_dosimeter.utils import (
    add_admin_id,
    delete_admin_id,
    get_admin_ids,
    get_avg_radiation_level,
    get_id_from_text,
    get_info_about_radiation_monitoring,
    get_info_about_region,
    get_points_with_radiation_level,
    get_uid,
    get_user_message,
    greeting,
)

__all__ = ("handler",)

logger = CustomAdapter(get_logger(__name__), {"user_id": get_uid()})


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
    def keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """Inline keyboard buttons handler"""
        query = update.callback_query
        match query.data:
            case Buttons.TOTAL_COUNT_USERS.callback_data:
                return self._get_count_users_callback(update, context)
            case Buttons.LIST_ADMIN.callback_data:
                return self._get_list_admin_ids_callback(update, context)
            case Buttons.ADD_ADMIN.callback_data | Buttons.DEL_ADMIN.callback_data:
                return self._enter_admin_by_user_id_callback(update, context)

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def message_callback(self, update: Update, context: CallbackContext) -> None:
        """Handler method for an incoming text messages from the user."""
        match update.message.text:
            case Buttons.MONITORING.label:
                return self._radiation_monitoring_callback(update, context)
            case Buttons.POINTS.label:
                button_list = (
                    Buttons.BREST,
                    Buttons.VITEBSK,
                    Buttons.MAIN_MENU,
                    Buttons.NEXT,
                )
                return self._monitoring_points_callback(update, context, button_list)
            case str() as command if command in (
                Buttons.NEXT.label,
                Buttons.NEXT_ARROW.label,
                Buttons.PREV.label,
                Buttons.PREV_ARROW.label,
            ):
                return self._manage_menu_callback(update, context, command)
            case Buttons.MAIN_MENU.label:
                return self._main_menu_callback(update, context)
            case Buttons.HIDE_KEYBOARD.label:
                return self._hide_keyboard_callback(update, context)
            case Buttons.BREST.label:
                points = Brest_region.monitoring_points
                action = Action.BREST
            case Buttons.VITEBSK.label:
                points = Vitebsk_region.monitoring_points
                action = Action.VITEBSK
            case Buttons.GOMEL.label:
                points = Gomel_region.monitoring_points
                action = Action.GOMEL
            case Buttons.GRODNO.label:
                points = Grodno_region.monitoring_points
                action = Action.GRODNO
            case Buttons.MINSK.label:
                points = Minsk_region.monitoring_points
                action = Action.MINSK
            case Buttons.MOGILEV.label:
                points = Mogilev_region.monitoring_points
                action = Action.MOGILEV
            case str() as user_id if user_id.startswith("add "):
                return self._add_admin_by_user_id_callback(update, context)
            case str() as user_id if user_id.startswith("del "):
                return self._delete_admin_by_user_id_callback(update, context)
            case _:
                return self._greeting_callback(update, context)

        return self._points_callback(update, context, points, action)

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

    def _manage_menu_callback(
        self, update: Update, context: CallbackContext, command: str
    ) -> None:
        """Handler method for generating keyboard buttons."""
        match command:
            case Buttons.NEXT.label:
                button_list = (
                    Buttons.GOMEL,
                    Buttons.GRODNO,
                    Buttons.PREV_ARROW,
                    Buttons.NEXT_ARROW,
                )
                action = Action.NEXT
            case Buttons.NEXT_ARROW.label:
                button_list = (
                    Buttons.MINSK,
                    Buttons.MOGILEV,
                    Buttons.PREV,
                    Buttons.MAIN_MENU,
                )
                action = Action.NEXT
            case Buttons.PREV.label:
                button_list = (
                    Buttons.GOMEL,
                    Buttons.GRODNO,
                    Buttons.PREV_ARROW,
                    Buttons.NEXT_ARROW,
                )
                action = Action.PREV
            case Buttons.PREV_ARROW.label:
                button_list = (
                    Buttons.BREST,
                    Buttons.VITEBSK,
                    Buttons.MAIN_MENU,
                    Buttons.NEXT,
                )
                action = Action.PREV
            case _:
                return self._main_menu_callback(update, context)

        keyboard = points_keyboard(button_list)
        return self._pagination_callback(update, context, keyboard, action)

    def _pagination_callback(
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

    def _greeting_callback(self, update: Update, context: CallbackContext) -> None:
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

    def _radiation_monitoring_callback(
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

    def _monitoring_points_callback(
        self, update: Update, context: CallbackContext, button_list: tuple[Buttons, ...]
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

    def _points_callback(
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

    def _main_menu_callback(self, update: Update, context: CallbackContext) -> None:
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

    def _get_count_users_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Get total count users admin command handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.repo.get_users_count(user),
        )
        logger.debug(self.LOG_MSG % Action.GET_COUNT.value, user_id=get_uid(user.id))

    def _get_list_admin_ids_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """An admin command handler method to get a list of admin IDs."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=get_admin_ids(),
        )
        logger.debug(self.LOG_MSG % Action.GET_LIST.value, user_id=get_uid(user.id))

    @staticmethod
    def _enter_admin_by_user_id_callback(
        update: Update, context: CallbackContext
    ) -> None:
        """
        The method of processing the administrator
        command for entering administrator IDs.
        """
        message = None
        query = update.callback_query
        match query.data:
            case Buttons.ADD_ADMIN.callback_data:
                message = Message.ADD_USER_ID
            case Buttons.DEL_ADMIN.callback_data:
                message = Message.DEL_USER_ID
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=message,
            reply_markup=ReplyKeyboardRemove(),
        )

    @restricted
    def _add_admin_by_user_id_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        An admin command handler method for adding a new admin
        to the temporary list of admin IDs.
        """
        user = update.effective_user
        forward_text, keyboard, log_msg = (None,) * 3
        match update.message.text:
            case str() as message if isinstance(uid := get_id_from_text(message), int):
                forward_text, success = add_admin_id(uid)
                log_msg = (
                    f"Added new user with ID - '{uid}' to the temp list of admins"
                    if success
                    else forward_text
                )
                keyboard = main_keyboard()
            case str() as message if isinstance(msg := get_id_from_text(message), str):
                forward_text, log_msg = (msg,) * 2
                keyboard = main_keyboard()

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=forward_text,
            reply_markup=keyboard,
        )
        logger.debug(log_msg, user_id=get_uid(user.id))

    @restricted
    def _delete_admin_by_user_id_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        An admin command handler method for deleting the admin
        to the temporary list of admin IDs.
        """
        user = update.effective_user
        forward_text, keyboard, log_msg = (None,) * 3
        match update.message.text:
            case str() as message if isinstance(uid := get_id_from_text(message), int):
                forward_text, success = delete_admin_id(uid)
                log_msg = (
                    f"Deleted user with ID - '{uid}' to the temp list of admins"
                    if success
                    else forward_text
                )
                keyboard = main_keyboard()
            case str() as message if isinstance(msg := get_id_from_text(message), str):
                forward_text, log_msg = (msg,) * 2
                keyboard = main_keyboard()

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=forward_text,
            reply_markup=keyboard,
        )
        logger.debug(log_msg, user_id=get_uid(user.id))

    def _hide_keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """Hide main keyboard handler method."""
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=Message.SHOW_KEYBOARD,
            reply_markup=ReplyKeyboardRemove(),
        )
        logger.debug(
            self.LOG_MSG % Action.HIDE_KEYBOARD.value, user_id=get_uid(user.id)
        )


"""Callback class instance"""
handler = Callback()
