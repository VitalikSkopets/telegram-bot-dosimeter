# type: ignore
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from dosimeter import config
from dosimeter.analytics import analytics
from dosimeter.analytics.decorators import analytic
from dosimeter.analytics.measurement_protocol import Analytics
from dosimeter.constants import ADMIN_ID, Action, Buttons, Points, Regions
from dosimeter.decorators import debug_handler, restricted, send_action
from dosimeter.geolocation import get_nearest_point_location
from dosimeter.keyboards import admin_keyboard, main_keyboard, points_keyboard
from dosimeter.message_engine import TemplateEngine, message_engine
from dosimeter.parse import parser
from dosimeter.parse.parser import Parser
from dosimeter.storage import file_manager_admins as f_manager
from dosimeter.storage import manager_admins as manager
from dosimeter.storage.mongodb import mongo_atlas__repo
from dosimeter.storage.repository import AdminManager, DocumentRepository
from dosimeter.utils import get_id_from_text, greeting

__all__ = ("Callback",)

logger = config.CustomAdapter(
    config.get_logger(__name__), {"user_id": manager.get_one()}
)


class Callback:
    """
    A class that encapsulates methods for processing Telegram bot commands.
    """

    LOG_MSG = "User selected '%s'"

    def __init__(
        self,
        parse: Parser = parser,
        template: TemplateEngine = message_engine,
        repo: DocumentRepository = mongo_atlas__repo,
        measurement: Analytics = analytics,
        control: AdminManager = manager or f_manager,
    ) -> None:
        """
        Constructor method for initializing objects of class Handlers.
        """
        self.parser = parse
        self.template = template
        self.repo = repo
        self.analytics = measurement
        self.manager = control

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @analytic(action=Action.START)
    def start_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Start command handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "start.html",
                user=user,
                button=Buttons,
            ),
            reply_markup=main_keyboard(),
        )
        self.repo.add_start(user)
        logger.info(
            self.LOG_MSG % Action.START.value, user_id=self.manager.get_one(user.id)
        )

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @analytic(action=Action.HELP)
    def help_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Help command handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render("help.html"),
            reply_markup=main_keyboard(),
        )
        self.repo.add_help(user)
        logger.info(
            self.LOG_MSG % Action.HELP.value, user_id=self.manager.get_one(user.id)
        )

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @restricted
    def admin_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Admin command handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render("admin.html"),
            reply_markup=admin_keyboard(),
        )
        logger.debug(
            self.LOG_MSG % Action.ADMIN.value, user_id=self.manager.get_one(user.id)
        )

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Inline keyboard buttons handler
        """
        match update.callback_query.data:
            case Buttons.TOTAL_COUNT_USERS.callback_data:
                return self._get_count_users_callback(update, context)
            case Buttons.LIST_ADMIN.callback_data:
                return self._get_list_admin_ids_callback(update, context)
            case Buttons.ADD_ADMIN.callback_data | Buttons.DEL_ADMIN.callback_data:
                return self._enter_admin_by_user_id_callback(update, context)

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def message_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for an incoming text messages from the user.
        """
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
                points = tuple(
                    point for point in Points if point.region == Regions.BREST
                )
                action = Action.BREST
            case Buttons.VITEBSK.label:
                points = tuple(
                    point for point in Points if point.region == Regions.VITEBSK
                )
                action = Action.VITEBSK
            case Buttons.GOMEL.label:
                points = tuple(
                    point for point in Points if point.region == Regions.GOMEL
                )
                action = Action.GOMEL
            case Buttons.GRODNO.label:
                points = tuple(
                    point for point in Points if point.region == Regions.GRODNO
                )
                action = Action.GRODNO
            case Buttons.MINSK.label:
                points = tuple(
                    point for point in Points if point.region == Regions.MINSK
                )
                action = Action.MINSK
            case Buttons.MOGILEV.label:
                points = tuple(
                    point for point in Points if point.region == Regions.MOGILEV
                )
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
    @analytic(action=Action.LOCATION)
    def send_location_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for pressing the "Send location" button by the user.
        """
        user = update.effective_user
        distance_to_nearest_point, nearest_point_name = get_nearest_point_location(
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
        )
        distance = f"{distance_to_nearest_point:,} м".replace(",", " ")

        for point, value in self.parser.get_points_with_radiation_level():
            if nearest_point_name == point:
                context.bot.send_message(
                    chat_id=update.effective_message.chat_id,
                    text=self.template.render(
                        "location.html",
                        distance=distance,
                        nearest_point=nearest_point_name,
                        point=point,
                        date=config.TODAY,
                        value=value,
                    ),
                )
                self.repo.add_location(user)
                logger.info(
                    self.LOG_MSG % Action.LOCATION.value,
                    user_id=self.manager.get_one(user.id),
                )
                break

    def _manage_menu_callback(
        self, update: Update, context: CallbackContext, command: str
    ) -> None:
        """
        Handler method for generating keyboard buttons.
        """
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
            text=self.template.render("region.html"),
            reply_markup=keyboard,
        )
        logger.info(self.LOG_MSG % action.value, user_id=self.manager.get_one(user.id))

    def _greeting_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for an incoming text message from the user.
        """
        user = update.effective_user
        message = update.message.text
        if message and message.lower() in greeting:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=self.template.render(
                    "greeting.html",
                    user=user,
                    button=Buttons,
                ),
                reply_markup=main_keyboard(),
            )
            self.repo.add_messages(user)
            self.analytics.send(
                user_id=user.id,
                user_lang_code=user.language_code,
                action=Action.GREETING.value,
            )
            logger.info(
                "User sent a welcome text message",
                user_id=self.manager.get_one(user.id),
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=self.template.render("unknown.html"),
            )
            self.analytics.send(
                user_id=user.id,
                user_lang_code=user.language_code,
                action=Action.MESSAGE.value,
            )
            logger.info(
                "User sent unknown text message", user_id=self.manager.get_one(user.id)
            )

    @analytic(action=Action.MONITORING)
    def _radiation_monitoring_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        Handler method for pressing the "Radiation monitoring" button by the user.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "radiation.html",
                date=config.TODAY,
                response=self.parser.get_info_about_radiation_monitoring(),
                value=self.parser.get_avg_radiation_level(),
            ),
        )
        self.repo.add_radiation_monitoring(user)
        logger.info(
            self.LOG_MSG % Action.MONITORING.value,
            user_id=self.manager.get_one(user.id),
        )

    @analytic(action=Action.POINTS)
    def _monitoring_points_callback(
        self, update: Update, context: CallbackContext, button_list: tuple[Buttons, ...]
    ) -> None:
        """
        Handler method for pressing the "Monitoring points" button by the user.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render("region.html"),
            reply_markup=points_keyboard(button_list),
        )
        self.repo.add_monitoring_points(user)
        logger.info(
            self.LOG_MSG % Action.POINTS.value, user_id=self.manager.get_one(user.id)
        )

    def _points_callback(
        self,
        update: Update,
        context: CallbackContext,
        points: tuple[Points, ...],
        action: Action,
    ) -> None:
        """
        Handler method for pressing the "* region" button by the user.
        """
        user = update.effective_user
        values_by_region, mean_value = self.parser.get_info_about_region(region=points)

        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "table.html",
                date=config.TODAY,
                values_by_region=values_by_region,
                mean_value=mean_value,
            ),
        )

        self.repo.add_region(user, action)
        self.analytics.send(
            user_id=user.id,
            user_lang_code=user.language_code,
            action=action.value,
        )
        logger.info(self.LOG_MSG % action.value, user_id=self.manager.get_one(user.id))

    @analytic(action=Action.MAIN_MENU)
    def _main_menu_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for pressing the "Main menu" button by the user.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "menu.html",
                user=user,
                button=Buttons,
            ),
            reply_markup=main_keyboard(),
        )
        logger.info(
            self.LOG_MSG % Action.MAIN_MENU.value, user_id=self.manager.get_one(user.id)
        )

    def _get_count_users_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        Get total count users admin command handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "count_of_users.html",
                value=self.repo.get_count_of_users(user),
            ),
        )
        logger.debug(
            self.LOG_MSG % Action.GET_COUNT.value, user_id=self.manager.get_one(user.id)
        )

    def _get_list_admin_ids_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        An admin command handler method to get a list of admin IDs.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(
                "list_of_admins.html",
                list_admins=self.manager.get_all(),
                main_admin=ADMIN_ID,
            ),
        )
        logger.debug(
            self.LOG_MSG % Action.GET_LIST.value, user_id=self.manager.get_one(user.id)
        )

    def _enter_admin_by_user_id_callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        The method of processing the administrator
        command for entering administrator IDs.
        """
        command = None
        query = update.callback_query
        match query.data:
            case Buttons.ADD_ADMIN.callback_data:
                command = "add"
            case Buttons.DEL_ADMIN.callback_data:
                command = "del"
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render("add_or_delete_user.html", command=command),
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
                forward_text, success = self.manager.add(uid)
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
        logger.debug(log_msg, user_id=self.manager.get_one(user.id))

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
                forward_text, success = self.manager.delete(uid)
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
        logger.debug(log_msg, user_id=self.manager.get_one(user.id))

    def _hide_keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Hide main keyboard handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render("show_keyboard.html"),
            reply_markup=ReplyKeyboardRemove(),
        )
        logger.debug(
            self.LOG_MSG % Action.HIDE_KEYBOARD.value,
            user_id=self.manager.get_one(user.id),
        )
