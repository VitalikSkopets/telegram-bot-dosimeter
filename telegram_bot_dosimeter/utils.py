import locale
from typing import Final

import requests  # type: ignore
import urllib3
from bs4 import BeautifulSoup
from emoji.core import emojize  # type: ignore
from fake_useragent import UserAgent
from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup, Update

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.constants import MonitoringPoint
from telegram_bot_dosimeter.logging_config import get_logger

__all__ = (
    "get_html",
    "get_cleaned_data",
    "greeting",
    "main_keyboard",
    "scraper",
    "text_messages",
)

logger = get_logger(__name__)

locale.setlocale(category=locale.LC_ALL, locale="Russian")
urllib3.disable_warnings()

commands = {
    "start": "Start using this bot",
    "help": "Useful information about this bot",
}

smile_radio: Final = emojize(":radioactive_sign:", use_aliases=True)
smile_robot: Final = emojize(":robot_face:", use_aliases=True)

text_messages: dict[str, str] = {
    "start": f"""
        \nЯ бот-дозиметр {smile_radio} \n\nЧтобы узнать по состоянию на _текущую
        дату_ уровень мощности эквивалентной дозы гамма-излучения,
        зафиксированного на _ближайшем_ пункте наблюдения, нажми *"Отправить
        мою геопозицию"*\n\nЧтобы узнать обстановку в сети радиационного
        мониторинга Беларуси, нажми *"Радиационный мониторинг"*\n\nЧтобы узнать
        сводку пунктов наблюдения в сети радиационного мониторинга, нажми *"Пункты
        наблюдения"* и выбери интересующий регион
        """,
    "help": """
        Бот-дозиметр может информировать пользователя по состоянию на
        _текущую дату_ о радиационной обстановке в Беларуси и об уровне
        мощности дозы (далее - МД) гамма-излучения, зафиксированного на
        _ближайшем_ к пользователю пункте наблюдения сети радиационного
        мониторинга Министерства природных ресурсов и охраны окружающей среды
        Беларуси (далее - Министерства) \n\nВ соответствии с приказом Министерства
        от 30.04.2021 №151-ОД, измерение уровней МД гамма-излучения проводится
        ежедневно в 06:00 часов по Гринвичскому времени дозиметрами или другими
        средствами измерения со статической погрешностью не более 20% \n\nДля оценки
        воздействия на организм человека используется понятие мощности эквивалентной
        дозы, которая измеряется в Зивертах/час\n\nВ быту можно считать, что 1
        Зиверт = 100 Рентген\n\n_Безопасным_ считается уровень радиации,
        приблизительно *до 0.5 мкЗв/ч*
        """,
    "greet": """
        \nЯ могу сообщать тебе информацию по состоянию на _текущую дату_ о об
        уровне мощности эквивалентной дозы (МД) гамма-излучения, зафиксированного на
        _ближайшем_ пункте наблюдения в сети радиационного мониторинга. Для
        этого нажми *"Отправить мою геопозицию"*\n\nЧтобы узнать обстановку в
        сети радиационного мониторинга Беларуси, нажми *"Радиационный
        мониторинг"*\n\nЧтобы узнать сводку пунктов наблюдения в сети
        радиационного мониторинга, нажми *"Пункты наблюдения"* и выбери
        интересующий регион
        """,
    "button1": "Отправить мою геопозицию",
    "button2": "Радиационный мониторинг",
    "info": f"""
        в настоящее время актуальная информация о состоянии радиационной обстановки
        недоступна. Попробуй спросить {smile_robot} в другой раз и обязательно увидишь
        ответ!
        """,
    "unknown": (
        f"Ничего не понятно, но очень интересно {smile_robot}\nПопробуй команду /help."
    ),
}

greeting: tuple[str, ...] = (
    "hello",
    "hi",
    "hey",
    "привет",
    "салют",
    "здарова",
    "здравствуй",
    "здравствуйте",
    "добрый день",
    "добрый вечер",
    "доброе утро",
    "доброго дня",
    "хелоу",
    "бонжур",
    "привестствую",
    "здрасте",
    "какая встреча",
    "рад встрече",
    "хай",
    "здравия желаю",
    "приветик",
    "доброго времени суток",
    "здорова",
    "здорово",
    "мое почтение",
    "приветствую тебя",
    "сердечно приветствую",
    "how are you",
    "what’s up",
    "whats up",
    "hello there",
    "howdy",
    "hiya",
    "yo",
    "how do you do",
    "good morning",
    "good afternoon",
    "good evening",
    "peek-a-boo",
    "peek a boo",
    "hi mister",
    "ahoy",
)


def get_html(url: str = config.URL_RADIATION) -> BeautifulSoup:
    """
    Function for scribing https://rad.org.by/radiation.xml

    :param url: string object with URL address 'https://rad.org.by/radiation.xml'

    :return: object bs4.BeautifulSoup class - web resource
    https://rad.org.by/radiation.xml html markup
    """
    response = requests.get(
        url,
        verify=False,
        headers={"User-Agent": UserAgent().random},
    )
    soup = BeautifulSoup(response.text, features="xml")
    return soup


def get_cleaned_data() -> list[tuple[str, str]]:
    """
    The function returns a list of tuples with the names of radiation monitoring
    points and values of the equivalent dose rate of gamma radiation.

    :return: List of tuples with the names of radiation monitoring
    points and values of the equivalent dose rate of gamma radiation.
    """
    soup: BeautifulSoup = get_html()

    points: list[str] = [point.text for point in soup.find_all("title")]
    points.reverse()

    values: list[str] = [value.text for value in soup.find_all("rad")]
    values.reverse()

    return list(zip(points, values))


def format_string(string: str, min_length: int = 20) -> str:
    """
    Функция увеличивает длину строкового объекта до 20 символов заполняя "-"
    пробельные символы

    :param string: строковый объект - название пункта наблюдения в сети радиационного
    мониторинга

    :param min_length: длина строкового объекта по умолчанию 20 симовлов

    :return: строковый объект (название пункта наблюдения) длиной 20 символов
    """
    while len(string) < min_length:
        string += "-"
    return string


def scraper(update: Update, region: tuple[MonitoringPoint]) -> None:
    """
    Функция вызывает метод get_html(), который отправляет GET-запрос и скрайпит
    HTML-структуру веб-ресурса https://rad.org.by/radiation.xml. Результаты
    скрайпинга в цикле for сравниваются на равенство с названиями пунктов наблюдения,
    расположенныъ в соответстсвующей области, и вместе с текущей датой подставляются
    в ответное сообщение пользователю. Также, функция расчитывает среднее
    арифметическое значение уровня радиации в сети соответствующих региоанльных
    пунктов радиационного мониторинга

    :param update: словарь Update с информацией о пользователе Telegram

    :param region: кортеж из объектов датакласса MonitoringPoint - пункты наблюдения
    из модуля constants.py

    :return: No-return
    """
    values_region: list[float] = []
    table: list[str] = []

    for point, value in get_cleaned_data():
        if point in [monitoring_point.name for monitoring_point in region]:
            values_region.append(float(value))
            table.append(
                f"""
                |`{format_string(point)}`|`{value + " мкЗв/ч":^13}`|
                """
            )
    update.message.reply_text(  # type: ignore
        "По состоянию на _{}_\n\n|`{:^20}`|`{:^13}`|\n".format(
            config.TODAY, "Пункт наблюдения", "Мощность дозы"
        )
        + "\n".join(table)
        + "\n\n*Среднее* значение уровня МД гамма-излучения в сети региоанльных"
        " пунктов радиационного мониторинга Министерства природных ресурсов и"
        " охраны окружающей среды Беларуси составляет *{:.1f}* мкЗв/ч.".format(
            sum(values_region) / len(values_region)
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard

    :return: The object of class telegram.ReplyKeyboardMarkup.
    """
    location_keyboard = KeyboardButton(
        "Отправить мою геопозицию", request_location=True
    )
    return ReplyKeyboardMarkup(
        (
            ["Радиационный мониторинг"],
            ["Пункты наблюдения"],
            [location_keyboard],
        ),
        resize_keyboard=True,
    )
