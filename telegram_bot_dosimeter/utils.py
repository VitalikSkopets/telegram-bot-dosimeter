import locale
from typing import Final

import requests  # type: ignore
import urllib3
from bs4 import BeautifulSoup
from emoji.core import emojize  # type: ignore
from fake_useragent import UserAgent
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.constants import MonitoringPoint
from telegram_bot_dosimeter.logging_config import get_logger

__all__ = (
    "get_html",
    "get_points_with_radiation_level",
    "get_avg_radiation_level",
    "get_info_about_radiation_monitoring",
    "greeting",
    "get_user_message",
    "main_keyboard",
    "get_info_about_region",
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
    Function for scribing HTML markup of the web resource.

    :param url: String object with HTML markup of the web resource.

    :return: Object of the class bs4.BeautifulSoup - HTML markup of the web resource.
    """
    response = requests.get(
        url,
        verify=False,
        headers={"User-Agent": UserAgent().random},
    )
    soup = BeautifulSoup(response.text, features="xml")
    return soup


def get_points_with_radiation_level(
    markup: BeautifulSoup | None = None,
) -> list[tuple[str, str]]:
    """
    The function returns a list of tuples with the names of radiation monitoring
    points and values of the equivalent dose rate of gamma radiation.

    :param markup: Object of the class bs4.BeautifulSoup - HTML markup of the web
    resource.

    :return: List of tuples with the names of radiation monitoring
    points and values of the equivalent dose rate of gamma radiation.
    """
    soup = markup or get_html()

    points: list[str] = [point.text for point in soup.find_all("title")]
    points.reverse()

    values: list[str] = [value.text for value in soup.find_all("rad")]
    values.reverse()

    return list(zip(points, values))


def get_avg_radiation_level() -> float:
    """
    The function returns the float value of the average level of radiation.

    :return: The value of the average level of radiation.
    """
    soup = get_html()
    rad_level: list[str] = [value.text for value in soup.find_all("rad")]
    rad_level.reverse()

    mean_level = sum([float(level) for level in rad_level]) / len(rad_level)

    return mean_level


def get_info_about_radiation_monitoring() -> str:
    """
    The function makes a GET request and scripts the html markup
    https://rad.org.by/monitoring/radiation.

    :return: String object.
    """
    markup = get_html(url=config.URL_MONITORING)
    lines = [span.text for span in markup.find_all("span")]
    data = """По состоянию на текущую дату радиационная обстановка на территории
    Республики Беларусь стабильная, мощность дозы гамма-излучения (МД) на пунктах
    наблюдений радиационного мониторинга атмосферного воздуха соответствует
    установившимся многолетним значениям. Как и прежде, повышенный уровень МД
    гамма-излучения зарегистрирован в пункте наблюдения города Брагин, находящегося в
    зоне радиоактивного загрязнения, обусловленного катастрофой на Чернобыльской АЭС.
    """
    cleaned_data = ""
    for line in lines:
        if line.startswith("По состоянию") and line.endswith("АЭС."):
            data = line.strip()
    if "натекущую датурадиационная" in data:
        cleaned_data = data.replace(
            "натекущую датурадиационная", "на текущую дату радиационная"
        )
    return cleaned_data or data


def format_string(string: str, min_length: int = 20) -> str:
    """
    The function increases the length of the string object to 20 characters by
    filling in "-" spaces.

    :param string: String object - the name of the observation point in the radiation
    monitoring network.

    :param min_length: Default string object length is 20 characters.

    :return: String object (observation point name) 20 characters long.
    """
    while len(string) < min_length:
        string += "-"
    return string


def get_info_about_region(
    region: tuple[MonitoringPoint],
) -> tuple[list[str], list[float]]:
    """
    The function calls the get_html() method, which sends a GET request and scripts
    the HTML markup of the https://rad.org.by/radiation.xml web resource. The results
    of scripting in the for loop are compared for equality with the names of the
    observation points located in the corresponding area, and together with the
    current date are substituted in the response message to the user. Also,
    the function calculates the arithmetic mean of the radiation level in the network
    of the corresponding regional radiation monitoring stations.

    :param region: Tuple of MonitoringPoint dataclass objects - monitoring points
    from the constants.py module.

    :return: No-return
    """
    values_by_region: list[float] = []
    table: list[str] = []

    for point, value in get_points_with_radiation_level():
        if point in [monitoring_point.name for monitoring_point in region]:
            values_by_region.append(float(value))
            table.append(
                f"""
                |`{format_string(point)}`|`{value + " мкЗв/ч":^13}`|
                """
            )
    return table, values_by_region


def get_user_message(table: list[str], values_by_region: list[float]) -> str:
    part_one = "По состоянию на _{}_\n\n|`{:^20}`|`{:^13}`|\n".format(
        config.TODAY, "Пункт наблюдения", "Мощность дозы"
    )
    part_two = "\n".join(table)
    part_three = "\n\n*Среднее* значение уровня МД гамма-излучения в сети региоанльных"
    " пунктов радиационного мониторинга Министерства природных ресурсов и"
    " охраны окружающей среды Беларуси составляет *{:.1f}* мкЗв/ч.".format(
        sum(values_by_region) / len(values_by_region)
    )
    return part_one + part_two + part_three


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard

    :return: The object of class telegram.ReplyKeyboardMarkup.
    """
    location_keyboard = KeyboardButton(
        "Отправить мою геопозицию", request_location=True
    )
    return ReplyKeyboardMarkup(
        [
            ["Радиационный мониторинг"],
            ["Пункты наблюдения"],
            [location_keyboard],
        ],
        resize_keyboard=True,
    )
