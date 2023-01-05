from typing import Final

import requests
import urllib3
from bs4 import BeautifulSoup
from emoji.core import emojize
from fake_useragent import UserAgent
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.config import get_logger
from telegram_bot_dosimeter.constants import LIST_OF_ADMIN_IDS, Button, MonitoringPoint

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
    "get_uid",
    "sos",
    "arrow",
)

logger = get_logger(__name__)

urllib3.disable_warnings()

radio: Final = emojize(":radioactive_sign:", use_aliases=True)
robot: Final = emojize(":robot_face:", use_aliases=True)
sos: Final = emojize(":SOS_button:", use_aliases=True)
arrow: Final = emojize(":right_arrow_curving_down:", use_aliases=True)

text_messages: dict[str, str] = {
    "start": "\nЯ бот-дозиметр {}\n\nЧтобы узнать по состоянию на <i>текущую "
    "дату</i> уровень мощности эквивалентной дозы гамма-излучения, "
    "зафиксированного на <i>ближайшем</i> пункте наблюдения, "
    "нажми <b>Отправить мою геопозицию</b>.\n\nЧтобы узнать "
    "обстановку в сети радиационного мониторинга Беларуси, "
    "нажми <b>Радиационный мониторинг</b>.\n\nЧтобы узнать сводку "
    "пунктов наблюдения в сети радиационного мониторинга, нажми <b>Пункты "
    "наблюдения</b> и выбери интересующий регион.".format(radio),
    "help": "Бот-дозиметр может информировать пользователя по состоянию на <i>текущую "
    "дату</i> о радиационной обстановке в Беларуси и об уровне мощности дозы "
    "(далее - МД) гамма-излучения, зафиксированного на <i>ближайшем</i> к "
    "пользователю пункте наблюдения сети радиационного мониторинга "
    "Министерства природных ресурсов и охраны окружающей среды Беларуси ("
    "далее - Министерства).\n\nВ соответствии с приказом Министерства от "
    "30.04.2021 №151-ОД, измерение уровней МД гамма-излучения проводится "
    "ежедневно в 06:00 часов по Гринвичскому времени дозиметрами или другими "
    "средствами измерения со статической погрешностью не более 20%.\n\nДля "
    "оценки воздействия на организм человека используется понятие мощности "
    "эквивалентной дозы, которая измеряется в Зивертах/час.\n\nВ быту можно "
    "считать, что 1 Зиверт = 100 Рентген.\n\n<i>Безопасным</i> считается "
    "уровень радиации, приблизительно <b>до 0.5 мкЗв/ч</b>.",
    "greet": "\nЯ могу сообщать тебе информацию по состоянию на <i>текущую дату</i> о "
    "об уровне мощности эквивалентной дозы (МД) гамма-излучения, "
    "зафиксированного на <i>ближайшем</i> пункте наблюдения в сети "
    "радиационного мониторинга. Для этого нажми <b>Отправить мою "
    "геопозицию</b>.\n\nЧтобы узнать обстановку в сети радиационного "
    "мониторинга Беларуси, нажми <b>Радиационный мониторинг</b>.\n\nЧтобы "
    "узнать сводку пунктов наблюдения в сети радиационного мониторинга, "
    "нажми <b>Пункты наблюдения</b> и выбери интересующий регион.",
    "desc": "<b>{}</b>, чтобы узнать по состоянию на <i>текущую дату</i> уровень "
    "мощности эквивалентной дозы гамма-излучения, зафиксированного на "
    "<i>ближайшем</i> пункте наблюдения, нажми <b>Отправить мою "
    "геопозицию</b>.\n\nЧтобы узнать обстановку в сети радиационного "
    "мониторинга Беларуси, нажми <b>Радиационный мониторинг</b>.\n\nЧтобы "
    "узнать сводку пунктов наблюдения в сети радиационного мониторинга, "
    "нажми <b>Пункты наблюдения</b> и выбери интересующий регион.",
    "location": "<i>{}</i> до ближайшего пункта наблюдения <b>{}</b>.\n\nВ пункте "
    "наблюдения <b>{}</b> по состоянию на <i>{}</i> уровень эквивалентной "
    "дозы радиации составляет <b>{}</b> мкЗв/ч.",
    "info": "в настоящее время актуальная информация о состоянии радиационной "
    "обстановки недоступна. Попробуй спросить {} в другой раз и обязательно "
    "получишь ответ!".format(robot),
    "unknown": "Ничего не понятно, но Оoоочень интересно {}\nПопробуй команду "
    "/help.".format(robot),
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


def get_html(url: str = config.URL_RADIATION) -> BeautifulSoup | None:
    """Function for scribing HTML markup of the web resource."""
    ua = UserAgent(
        browsers=["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
    )
    response = None
    try:
        response = requests.get(url, verify=False, headers={"User-Agent": ua.random})
    except Exception as ex:
        logger.exception(
            "Unable to connect to the URL: %s. Raised exception: %s" % (url, ex)
        )

    soup = BeautifulSoup(response.text, features="lxml-xml") if response else None
    return soup


def get_points_with_radiation_level(
    markup: BeautifulSoup | None = None,
) -> list[tuple[str, str]]:
    """
    The function returns a list of tuples with the names of radiation monitoring
    points and values of the equivalent dose rate of gamma radiation.
    """
    soup = markup or get_html()

    points: list[str] = [point.text for point in soup.find_all("title")]  # type: ignore
    points.reverse()

    values: list[str] = [value.text for value in soup.find_all("rad")]  # type: ignore
    values.reverse()

    return list(zip(points, values))


def get_avg_radiation_level() -> float:
    """The function returns the float value of the average level of radiation."""
    soup = get_html()
    rad_level: list[str] = [val.text for val in soup.find_all("rad")]  # type: ignore
    rad_level.reverse()

    mean_level = sum([float(level) for level in rad_level]) / len(rad_level)

    return mean_level


def get_info_about_radiation_monitoring() -> str | None:
    """
    The function makes a GET request and scripts the html markup
    https://rad.org.by/monitoring/radiation.
    """
    markup = get_html(url=config.URL_MONITORING)
    lines = [span.text for span in markup.find_all("span")]  # type: ignore
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
    """
    while len(string) < min_length:
        string += "-"
    return string


def get_info_about_region(
    region: tuple[MonitoringPoint, ...],
) -> tuple[list[str], list[float]]:
    """
    The function calls the get_html() method, which sends a GET request and scripts
    the HTML markup of the https://rad.org.by/radiation.xml web resource. The results
    of scripting in the for loop are compared for equality with the names of the
    observation points located in the corresponding area, and together with the
    current date are substituted in the response message to the user. Also,
    the function calculates the arithmetic mean of the radiation level in the network
    of the corresponding regional radiation monitoring stations.
    """
    line = "|<code>{}</code>|<code>{:^13}</code>|"
    values_by_region: list[float] = []
    table: list[str] = []

    for point, value in get_points_with_radiation_level():
        if point in [monitoring_point.name for monitoring_point in region]:
            values_by_region.append(float(value))
            table.append(line.format(format_string(point), value + " мкЗв/ч"))
    return table, values_by_region


def get_user_message(table: list[str], values: list[float]) -> str:
    line = "По состоянию на <i>{}</i>\n\n|<code>{:^20}</code>|<code>{:^13}</code>|\n"
    part_1 = line.format(config.TODAY, "Пункт наблюдения", "Мощность дозы")
    part_2 = "\n".join(table)
    line2 = (
        "\n\n<b>Среднее</b> значение уровня МД гамма-излучения в сети "
        "региоанльных пунктов радиационного мониторинга Министерства природных "
        "ресурсов и охраны окружающей среды Беларуси составляет <b>{:.1f}</b> "
        "мкЗв/ч. "
    )
    part_3 = line2.format(sum(values) / len(values))
    return part_1 + part_2 + part_3


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard
    """
    location_keyboard = KeyboardButton(Button.SEND_LOCATION, request_location=True)
    return ReplyKeyboardMarkup(
        [
            [Button.MONITORING],
            [Button.POINTS],
            [location_keyboard],
        ],
        resize_keyboard=True,
    )


def get_uid(uid: str | int | None = None) -> str | int | None:
    if uid and int(uid) not in LIST_OF_ADMIN_IDS:
        return int(uid)
    if uid and int(uid) in LIST_OF_ADMIN_IDS:
        return "ADMIN"
    return None
