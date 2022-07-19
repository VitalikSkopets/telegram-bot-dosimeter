import re

from geopy import distance
from telegram import ChatAction, ParseMode, ReplyKeyboardMarkup, Update, User
from telegram.ext import CallbackContext

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.analytics.measurement_protocol import send_analytics
from telegram_bot_dosimeter.constants import (
    MONITORING_POINTS,
    Brest_region,
    Gomel_region,
    Grodno_region,
    Minsk_region,
    Mogilev_region,
    Vitebsk_region,
)
from telegram_bot_dosimeter.decorators import debug_handler, send_action
from telegram_bot_dosimeter.logging_config import get_logger
from telegram_bot_dosimeter.main import command_handler
from telegram_bot_dosimeter.storage.mongodb import MongoDataBase
from telegram_bot_dosimeter.utils import (
    get_cleaned_data,
    get_html,
    greeting,
    main_keyboard,
    scraper,
    text_messages,
)

__all__ = ("Callback",)

logger = get_logger(__name__)

MongoDB = MongoDataBase()


class Callback:
    """
    Класс, инкапсулирующий методы обработки команд Telegram-бота
    """

    def __init__(self, storage: MongoDataBase = MongoDB) -> None:
        """
        Метод-конструктор для инициализации объектов класса Handlers

        :param storage: object pymongo.MongoClient class для
        соединения с базой данных users_db в MongoDB Atlas

        """
        self.repo = storage
        self.update = Update
        self.context = CallbackContext
        self.user: User = self.update.message.from_user  # type: ignore

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    @command_handler("start")
    def start_callback(self) -> None:
        """
        Метод-обработчик команды Start. При выборе пользователем команды Start
        возвращает приветственное сообщение и кнопки меню Telegram-бота вместо
        стандартной клавиатуры

        :return: Non-return
        """
        start_message = text_messages.get("start")
        self.update.message.reply_text(  # type: ignore
            f"""
            Рад нашему знакомству, *{self.user.first_name}*!{start_message}
            """,
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
        """
        Метод-обработчик команды Help. При выборе пользователем команды Help
        возвращает текстовое сообщение и кнопки меню вместо стандартной клавиатуры

        :return: Non-return
        """
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
        """
        Метод-обработчик входящего текстового сообщения от пользователя. Если в
        текстовом сообщении пользователя есть строка из списка greeting, метод
        возвращает пользователю приветственное текстовое сообщение и кнопки меню
        вместо стандартной клавиатуры. Если в сообщении пользователя строки
        невходящие в список greeting, метод возвращает пользователю текстовое
        сообщение с предложением выбрать команду Help

        :return: Non-return
        """
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
        """
        Метод-обработчик нажатия кнопки "Радиационный мониторинг". В теле метода
        вызывается кастомная функцию get_html(), которая осуществляет GET-запрос и
        скрайпит html-структуру https://rad.org.by/monitoring/radiation на основе
        регулярного выражения. Результаты скрайпинга в виде строкового объекта вместе
        с текущей датой подставляются в интерполированную строку - ответное сообщение
        пользователю. Также, в теле метода происходит повторный вызов кастомной
        функцию get_html(), которая в результате скрайпинга
        https://rad.org.by/radiation.xml возвращает строковые значения радиации всех
        пунктов наблюдения, после чего приводит строковые значения уровня радиации к
        типу данных float и расчитывает среднее арефметическое значение уровня
        радиации всех пунктов наблюдения. Среднее арефметическое значение уровня
        радиации, также подставляются в интерполированную строку - ответное сообщение
        пользователю

        :return: Non-return
        """
        text_lst = str(get_html(url=config.URL_MONITORING).find_all("span"))
        pattern = r"(?:...*)(радиационная...*АЭС.)(?:<\/span>)"
        text = re.findall(pattern, text_lst)
        values = get_html().find_all("rad")
        mean = sum([float(indication.text) for indication in values]) / len(values)
        self.update.message.reply_text(  # type: ignore
            f"""
            По состоянию на _{config.TODAY}_ {text[0]}\n\nПо стране
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
        """
        Метод-обработчик нажатия пользователем кнопки "Пункты наблюдения".
        Возвращает пользователю кнопки меню с названиями областей вместо стандартной
        клавиатуры

        :return: Non-return
        """
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
        """
        Метод-обработчик нажатия пользователем кнопки "Брестская область". Метод
        вызывет фунцию scraper(), которая, в свою очередь, вызывает функцию get_html().
        Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Брестской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: Non-return
        """
        scraper(self.update, region=Brest_region.monitoring_points)  # type: ignore
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
        """
        Метод-обработчик нажатия пользователем кнопки "Витебская область". Метод
        вызывет функцию scraper(), которая, в свою очередь, вызывает функцию get_html().
        Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Витебской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: Non-return
        """
        user: User = self.update.effective_user  # type: ignore
        scraper(self.update, region=Vitebsk_region.monitoring_points)  # type: ignore
        self.repo.add_region(user, "Vitebsk region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Vitebsk region",
        )
        logger.info(f'User {self.user.id} press button "Vitebsk region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def gomel_callback(self) -> None:
        """
        Метод-обработчик нажатия пользователем кнопки "Гомельская область". Метод
        вызывет функцию scraper(), которая, в свою очередь, вызывает функцию get_html().
        Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Гомельской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: Non-return
        """
        scraper(self.update, region=Gomel_region.monitoring_points)  # type: ignore
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
        """
        Метод-обработчик нажатия пользователем кнопки "Гродненская область".
        Метод вызывет функцию scraper(), которая, в свою очередь, вызывает функцию
        get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Гродненской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: non-return
        """
        scraper(self.update, region=Grodno_region.monitoring_points)  # type: ignore
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
        """
        Метод-обработчик нажатия пользователем кнопки "Минск и Минская область".
        Метод вызывет функцию scraper(), которая, в свою очередь, вызывает функцию
        get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Минске и Минской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: Non-return
        """
        scraper(self.update, region=Minsk_region.monitoring_points)  # type: ignore
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
        """
        Метод-обработчик нажатия пользователем кнопки "Могилевская область".
        Метод вызывет функцию scraper(), которая, в свою очередь, вызывает функцию
        get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for
        сравниваются на равенство с названиями пунктов наблюдения, расположенных в
        Могилевскойй области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :return: None
        """
        scraper(self.update, region=Mogilev_region.monitoring_points)  # type: ignore
        self.repo.add_region(self.user, "Mogilev region")
        send_analytics(
            user_id=self.user.id,
            user_lang_code=self.user.language_code,  # type: ignore
            action_name="Mogilev region",
        )
        logger.info(f'User {self.user.id} press button "Mogilev region"')

    @debug_handler(log_handler=logger)
    @send_action(ChatAction.TYPING)
    def main_menu_callback(self) -> None:
        """
        Метод-обработчик нажатия пользователем кнопки "Главное меню". В качестве
        ответного сообщения пользователю обработчик вызывает кастомную функцию
        main_keyboard(), которая возвращает пользователю сообщение и кнопки меню
        вместо стандартной клавиатуры

        :return: Non-return
        """
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
        """
        Метод-обработчик нажатия кнопки "Отправить мою геолокацию". В теле метода
        происходит вызов aeyrwbb distance() из библиотеки geopy, которому в качестве
        оргументов передаются географические координаты пользователя и пунктов
        наблюдения из словаря MONITORING_POINTS. Метод distance() расчитывает
        расстояние в метрах от каждого пункта наблюдения до пользователя. С помощью
        встроенной функции min() определяется расстояние до ближайшего к пользователю
        пунтка наблюдения. Также, в теле функция производит вызов кастомной функцию
        get_html(), которая осуществляет скрайпинг html-структуры
        https://rad.org.by/radiation.xml. Результаты выполнения метода distance() и
        функции скрайпинга вместе с текущей датой и временем подставляются в
        интерполированную строку, которая отправляется пользователю в качестве
        ответного сообщения

        :return: Non-return
        """
        user_coordinates: tuple[float, float] = (
            self.update.message.location.latitude,  # type: ignore
            self.update.message.location.longitude,  # type: ignore
        )
        distance_list: list[tuple[float, str]] = []
        for point in MONITORING_POINTS:
            distance_list.append(
                (
                    distance.distance(user_coordinates, point.coordinates).km,
                    point.name,
                ),
            )
        min_distance: tuple[float, str] = min(distance_list)

        for point, value in get_cleaned_data():  # type: ignore
            if min_distance[1] == point:
                self.update.message.reply_text(  # type: ignore
                    f"""
                    _{min_distance[0]:.3f} м_ до ближайшего пункта наблюдения
                    "{min_distance[1]}".\n\nВ пункте наблюдения "{point}"
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
