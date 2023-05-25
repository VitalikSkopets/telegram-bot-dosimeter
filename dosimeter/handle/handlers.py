# type: ignore
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from dosimeter.analytics import Analytics, analytics
from dosimeter.analytics.decorators import analytic
from dosimeter.config import settings
from dosimeter.config.logger import CustomAdapter, get_logger
from dosimeter.constants import ADMIN_ID, Action, Button, Point, Region
from dosimeter.navigator import Navigator, navigator
from dosimeter.parse import Parser, parser
from dosimeter.storage import file_manager_admins as f_manager
from dosimeter.storage import manager_admins as manager
from dosimeter.storage.mongo import mongo_atlas__repo
from dosimeter.storage.repository import AdminManager, Repository
from dosimeter.template_engine import TemplateEngine, message_engine
from dosimeter.template_engine.engine import Template
from dosimeter.utils import keyboards, utils
from dosimeter.utils.decorators import debug_handler, restricted, send_action

__all__ = ("Handler",)

logger = CustomAdapter(get_logger(__name__), {"user_id": manager.get_one()})


class Handler(object):
    """
    A class that encapsulates methods for processing Telegram bot commands.
    """

    LOG_MSG = "User selected '%s'"

    def __init__(
        self,
        parse: Parser = parser,
        template: TemplateEngine = message_engine,
        repo: Repository = mongo_atlas__repo,
        geolocation: Navigator = navigator,
        measurement: Analytics = analytics,
        control: AdminManager = manager or f_manager,
    ) -> None:
        """
        Constructor method for initializing objects of class Handlers.
        """
        self.parser = parse
        self.template = template
        self.repo = repo
        self.navigator = geolocation
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
                Template.START,
                user=user,
                button=Button,
            ),
            reply_markup=keyboards.main_keyboard(),
        )
        self.repo.put(user, Action.START)
        logger.info(self.LOG_MSG % Action.START, user_id=self.manager.get_one(user.id))

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
            text=self.template.render(Template.HELP),
            reply_markup=keyboards.main_keyboard(),
        )
        self.repo.put(user, Action.HELP)
        logger.info(self.LOG_MSG % Action.HELP, user_id=self.manager.get_one(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @analytic(action=Action.DONATE)
    def donate_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Donate command handler method.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(Template.DONATE),
            reply_markup=keyboards.donate_keyboard(),
        )
        self.repo.put(user, Action.DONATE)
        logger.debug(
            self.LOG_MSG % Action.DONATE, user_id=self.manager.get_one(user.id)
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
            text=self.template.render(Template.ADMIN),
            reply_markup=keyboards.admin_keyboard(),
        )
        logger.debug(self.LOG_MSG % Action.ADMIN, user_id=self.manager.get_one(user.id))

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def keyboard_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Inline keyboard buttons handler
        """
        match update.callback_query.data:
            case Button.TOTAL_COUNT_USERS.callback_data:
                return self._get_count_users_callback(update, context)
            case Button.LIST_ADMIN.callback_data:
                return self._get_list_admin_ids_callback(update, context)
            case Button.ADD_ADMIN.callback_data | Button.DEL_ADMIN.callback_data:
                return self._enter_admin_by_user_id_callback(update, context)

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def message_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for an incoming text messages from the user.
        """
        match update.message.text:
            case Button.MONITORING.label:
                return self._radiation_monitoring_callback(update, context)
            case Button.POINTS.label:
                button_list = (
                    Button.BREST,
                    Button.VITEBSK,
                    Button.MAIN_MENU,
                    Button.NEXT,
                )
                return self._monitoring_points_callback(update, context, button_list)
            case str() as command if command in (
                Button.NEXT.label,
                Button.NEXT_ARROW.label,
                Button.PREV.label,
                Button.PREV_ARROW.label,
            ):
                return self._manage_menu_callback(update, context, command)
            case Button.MAIN_MENU.label:
                return self._main_menu_callback(update, context)
            case Button.HIDE_KEYBOARD.label:
                return self._hide_keyboard_callback(update, context)
            case Button.BREST.label:
                points = tuple(point for point in Point if point.region == Region.BREST)
                action = Action.BREST
            case Button.VITEBSK.label:
                points = tuple(
                    point for point in Point if point.region == Region.VITEBSK
                )
                action = Action.VITEBSK
            case Button.GOMEL.label:
                points = tuple(point for point in Point if point.region == Region.GOMEL)
                action = Action.GOMEL
            case Button.GRODNO.label:
                points = tuple(
                    point for point in Point if point.region == Region.GRODNO
                )
                action = Action.GRODNO
            case Button.MINSK.label:
                points = tuple(point for point in Point if point.region == Region.MINSK)
                action = Action.MINSK
            case Button.MOGILEV.label:
                points = tuple(
                    point for point in Point if point.region == Region.MOGILEV
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
        near_point = self.navigator.get_near_point(
            user.id,
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
        )

        for point, value in self.parser.get_points_with_radiation_level().items():
            if near_point.title == point:
                context.bot.send_message(
                    chat_id=update.effective_message.chat_id,
                    text=self.template.render(
                        Template.LOCATION,
                        distance=f"{near_point.distance:,} м".replace(",", " "),
                        point=near_point.title,
                        date=settings.TODAY,
                        value=value,
                    ),
                )
                self.repo.put(user, Action.LOCATION)
                logger.info(
                    self.LOG_MSG % Action.LOCATION,
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
            case Button.NEXT.label:
                button_list = (
                    Button.GOMEL,
                    Button.GRODNO,
                    Button.PREV_ARROW,
                    Button.NEXT_ARROW,
                )
                action = Action.NEXT
            case Button.NEXT_ARROW.label:
                button_list = (
                    Button.MINSK,
                    Button.MOGILEV,
                    Button.PREV,
                    Button.MAIN_MENU,
                )
                action = Action.NEXT
            case Button.PREV.label:
                button_list = (
                    Button.GOMEL,
                    Button.GRODNO,
                    Button.PREV_ARROW,
                    Button.NEXT_ARROW,
                )
                action = Action.PREV
            case Button.PREV_ARROW.label:
                button_list = (
                    Button.BREST,
                    Button.VITEBSK,
                    Button.MAIN_MENU,
                    Button.NEXT,
                )
                action = Action.PREV
            case _:
                return self._main_menu_callback(update, context)

        keyboard = keyboards.points_keyboard(button_list)
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
            text=self.template.render(Template.REGION),
            reply_markup=keyboard,
        )
        logger.info(self.LOG_MSG % action.value, user_id=self.manager.get_one(user.id))

    def _greeting_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Handler method for an incoming text message from the user.
        """
        user = update.effective_user
        message = update.message.text
        if message and message.lower() in utils.greeting:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=self.template.render(
                    Template.GREET,
                    user=user,
                    button=Button,
                ),
                reply_markup=keyboards.main_keyboard(),
            )
            self.repo.put(user, Action.GREETING)
            self.analytics.send(
                user_id=user.id,
                user_lang_code=user.language_code,
                action=Action.GREETING,
            )
            logger.info(
                "User sent a welcome text message",
                user_id=self.manager.get_one(user.id),
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=self.template.render(Template.UNKNOWN),
            )
            self.analytics.send(
                user_id=user.id,
                user_lang_code=user.language_code,
                action=Action.MESSAGE,
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
                Template.RADIATION,
                date=settings.TODAY,
                response=self.parser.get_info_about_radiation_monitoring(),
                value=self.parser.get_mean_radiation_level(),
            ),
        )
        self.repo.put(user, Action.MONITORING)
        logger.info(
            self.LOG_MSG % Action.MONITORING,
            user_id=self.manager.get_one(user.id),
        )

    @analytic(action=Action.POINTS)
    def _monitoring_points_callback(
        self, update: Update, context: CallbackContext, button_list: tuple[Button, ...]
    ) -> None:
        """
        Handler method for pressing the "Monitoring points" button by the user.
        """
        user = update.effective_user
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(Template.REGION),
            reply_markup=keyboards.points_keyboard(button_list),
        )
        self.repo.put(user, Action.POINTS)
        logger.info(self.LOG_MSG % Action.POINTS, user_id=self.manager.get_one(user.id))

    def _points_callback(
        self,
        update: Update,
        context: CallbackContext,
        points: tuple[Point, ...],
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
                Template.TABLE,
                date=settings.TODAY,
                values_by_region=values_by_region,
                mean_value=mean_value,
            ),
        )

        self.repo.put(user, action)
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
                Template.MENU,
                user=user,
                button=Button,
            ),
            reply_markup=keyboards.main_keyboard(),
        )
        logger.info(
            self.LOG_MSG % Action.MAIN_MENU, user_id=self.manager.get_one(user.id)
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
                Template.USER_COUNT,
                value=self.repo.get_count_of_users(user),
            ),
        )
        logger.debug(
            self.LOG_MSG % Action.GET_COUNT, user_id=self.manager.get_one(user.id)
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
                Template.ADMINS_LIST,
                list_admins=self.manager.get_all(),
                main_admin=ADMIN_ID,
            ),
        )
        logger.debug(
            self.LOG_MSG % Action.GET_LIST, user_id=self.manager.get_one(user.id)
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
            case Button.ADD_ADMIN.callback_data:
                command = "add"
            case Button.DEL_ADMIN.callback_data:
                command = "del"
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=self.template.render(Template.ADD_OR_DEL_USER, command=command),
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
            case str() as message if isinstance(
                uid := utils.get_id_from_text(message), int
            ):
                forward_text, success = self.manager.add(uid)
                log_msg = (
                    f"Added new user with ID - '{uid}' to the temp list of admins"
                    if success
                    else forward_text
                )
                keyboard = keyboards.main_keyboard()
            case str() as message if isinstance(
                msg := utils.get_id_from_text(message), str
            ):
                forward_text, log_msg = (msg,) * 2
                keyboard = keyboards.main_keyboard()

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
            case str() as message if isinstance(
                uid := utils.get_id_from_text(message), int
            ):
                forward_text, success = self.manager.delete(uid)
                log_msg = (
                    f"Deleted user with ID - '{uid}' to the temp list of admins"
                    if success
                    else forward_text
                )
                keyboard = keyboards.main_keyboard()
            case str() as message if isinstance(
                msg := utils.get_id_from_text(message), str
            ):
                forward_text, log_msg = (msg,) * 2
                keyboard = keyboards.main_keyboard()

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
            text=self.template.render(Template.KEYBOARD),
            reply_markup=ReplyKeyboardRemove(),
        )
        logger.debug(
            self.LOG_MSG % Action.HIDE_KEYBOARD,
            user_id=self.manager.get_one(user.id),
        )
