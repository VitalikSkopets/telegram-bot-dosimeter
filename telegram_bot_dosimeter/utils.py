import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from telegram_bot_dosimeter import config
from telegram_bot_dosimeter.config import get_logger
from telegram_bot_dosimeter.constants import (
    ADMIN_ID,
    LIST_OF_ADMIN_IDS,
    MonitoringPoint,
)
from telegram_bot_dosimeter.messages import Message

__all__ = (
    "get_html",
    "get_points_with_radiation_level",
    "get_avg_radiation_level",
    "get_info_about_radiation_monitoring",
    "greeting",
    "get_user_message",
    "get_info_about_region",
    "get_uid",
    "get_admin_ids",
)

logger = get_logger(__name__)

urllib3.disable_warnings()

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
    data = Message.MONITORING
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
    line = Message.TABLE
    part_1 = line.format(config.TODAY, "Пункт наблюдения", "Мощность дозы")
    part_2 = "\n".join(table)
    line2 = Message.AVG
    part_3 = line2.format(sum(values) / len(values))
    return part_1 + part_2 + part_3


def get_uid(uid: str | int | None = None) -> str | int | None:
    if uid and int(uid) not in LIST_OF_ADMIN_IDS:
        return int(uid)
    if uid and int(uid) in LIST_OF_ADMIN_IDS:
        return "ADMIN"
    return None


def get_admin_ids() -> str:
    if not LIST_OF_ADMIN_IDS:
        return "Admins not assigned"
    output = []
    for num, admin_id in enumerate(LIST_OF_ADMIN_IDS, 1):
        message = "{}: {} - Main admin" if admin_id == ADMIN_ID else "{}: {}"
        output.append(message.format(num, admin_id))
    return "\n".join(output)
