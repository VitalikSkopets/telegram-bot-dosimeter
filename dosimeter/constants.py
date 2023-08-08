import enum
import uuid
from dataclasses import dataclass
from typing import TypeAlias, TypedDict
from urllib.parse import ParseResult, urlparse

from emoji.core import emojize

from dosimeter.config import config

__all__ = (
    "ADMIN_ID",
    "LIST_OF_ADMIN_IDS",
    "TEMP_LIST_OF_ADMIN_IDS",
    "URL",
    "Action",
    "Button",
    "Command",
    "Emoji",
    "Point",
    "Region",
)

Coordinates: TypeAlias = tuple[float, float]

ADMIN_ID: int = config.app.main_admin_tgm_id or config.app.admin_tgm_id
LIST_OF_ADMIN_IDS: tuple[int, int] = (ADMIN_ID, 487236325)
TEMP_LIST_OF_ADMIN_IDS: list[int] = []


@dataclass(frozen=True)
class BotInfo:
    DESCRIPTION: str = """
    Этот бот может информировать пользователя по состоянию на текущую дату о
    радиационной обстановке в Беларуси и об уровне мощности эквивалентной дозы
    гамма-излучения, зафиксированного в сети радиационного мониторинга Министерства
    природных ресурсов и охраны окружающей среды Беларуси.

    Источник: ©rad.org.by
    Разработано: ©itrexgroup.com
    """
    ABOUT: str = """
    Бот информирует об обстановке в сети радиационного мониторинга Беларуси.
    """
    START: str = "Launch this bot / Запустить бота"
    HELP: str = "Useful info about this bot / Полезная информация о боте"
    ADMIN: str = "List of admin commands (limited access)"
    DONATE: str = "Buy me a coffee"


class URL(str, enum.Enum):
    RADIATION = urlparse(f"{config.app.source}/radiation.xml").geturl()
    MONITORING = urlparse(f"{config.app.source}/monitoring/radiation").geturl()

    def __str__(self) -> str:
        return self.value


class Region(str, enum.Enum):
    BREST = "Брестская область"
    VITEBSK = "Витебская область"
    GOMEL = "Гомельская область"
    GRODNO = "Гродненская область"
    MOGILEV = "Могилевская область"
    MINSK = "Минск и Минская область"

    def __str__(self) -> str:
        return self.value


class PointSchema(TypedDict):
    """
    Schema for Point.
    """

    label: str
    latitude: float
    longitude: float
    region: Region


class Point(enum.Enum):
    MOGILEV = PointSchema(
        label="Могилев",
        latitude=30.375068475712993,
        longitude=53.69298772769127,
        region=Region.MOGILEV,
    )

    MSTISLAVL = PointSchema(
        label="Мстиславль",
        latitude=31.742790754635983,
        longitude=54.025123497951235,
        region=Region.MOGILEV,
    )

    POLOTSK = PointSchema(
        label="Полоцк",
        latitude=28.751296645976183,
        longitude=55.47475184602021,
        region=Region.VITEBSK,
    )

    SHARKOVSHCHINA = PointSchema(
        label="Шарковщина",
        latitude=27.456996363944278,
        longitude=55.36281482842422,
        region=Region.VITEBSK,
    )

    MINSK = PointSchema(
        label="Минск",
        latitude=27.63548838979854,
        longitude=53.92751824354786,
        region=Region.MINSK,
    )

    LYNTUPY = PointSchema(
        label="Лынтупы",
        latitude=26.306634538263953,
        longitude=55.04878637860638,
        region=Region.VITEBSK,
    )

    VISOKOE = PointSchema(
        label="Высокое",
        latitude=23.38374438625246,
        longitude=52.366928433095,
        region=Region.BREST,
    )

    PRUZHANY = PointSchema(
        label="Пружаны",
        latitude=24.48545241420398,
        longitude=52.567268449727045,
        region=Region.BREST,
    )

    SLUTSK = PointSchema(
        label="Слуцк",
        latitude=27.552283199561725,
        longitude=53.05284098247522,
        region=Region.MINSK,
    )

    BRAGIN = PointSchema(
        label="Брагин",
        latitude=30.246689891878724,
        longitude=51.7969974359342,
        region=Region.GOMEL,
    )

    ORSHA = PointSchema(
        label="Орша",
        latitude=30.443815788156527,
        longitude=54.503170699795774,
        region=Region.VITEBSK,
    )

    MOZYR = PointSchema(
        label="Мозырь",
        latitude=29.1925370196736,
        longitude=52.036635775856084,
        region=Region.GOMEL,
    )

    SLAVGOROD = PointSchema(
        label="Славгород",
        latitude=31.003458658160586,
        longitude=53.45088516337511,
        region=Region.MOGILEV,
    )

    VASILEVICHI = PointSchema(
        label="Василевичи",
        latitude=29.838848231201965,
        longitude=52.25207675198943,
        region=Region.GOMEL,
    )

    ZHLOBIN = PointSchema(
        label="Жлобин",
        latitude=30.043705893277984,
        longitude=52.89414619807851,
        region=Region.GOMEL,
    )

    GORKI = PointSchema(
        label="Горки",
        latitude=30.94344246329931,
        longitude=54.30393502455042,
        region=Region.MOGILEV,
    )

    VOLKOVYSK = PointSchema(
        label="Волковыск",
        latitude=24.448995268762964,
        longitude=53.16692103793095,
        region=Region.GRODNO,
    )

    OKTYABR = PointSchema(
        label="Октябрь",
        latitude=28.883476209528087,
        longitude=52.63342658653018,
        region=Region.GOMEL,
    )

    KOSTYUKOVICHI = PointSchema(
        label="Костюковичи",
        latitude=32.070027796122154,
        longitude=53.35847386774336,
        region=Region.MOGILEV,
    )

    BREST = PointSchema(
        label="Брест",
        latitude=23.685652135212752,
        longitude=52.116580901478635,
        region=Region.BREST,
    )

    BOBRUISK = PointSchema(
        label="Бобруйск",
        latitude=29.127272432117724,
        longitude=53.20853347538013,
        region=Region.MOGILEV,
    )

    IVATSEVICHI = PointSchema(
        label="Ивацевичи",
        latitude=25.350471424000386,
        longitude=52.716654759080775,
        region=Region.BREST,
    )

    VILEYKA = PointSchema(
        label="Вилейка",
        latitude=26.89989831916185,
        longitude=54.48321442087189,
        region=Region.MINSK,
    )

    BORISOV = PointSchema(
        label="Борисов",
        latitude=28.49760585109516,
        longitude=54.26563317790094,
        region=Region.MINSK,
    )

    ZHITKOVICHI = PointSchema(
        label="Житковичи",
        latitude=27.870082634924596,
        longitude=52.21411222651425,
        region=Region.GOMEL,
    )

    OSHMYANY = PointSchema(
        label="Ошмяны",
        latitude=25.935350063150867,
        longitude=54.43300284193779,
        region=Region.GRODNO,
    )

    BEREZINO = PointSchema(
        label="Березино",
        latitude=28.99727106523084,
        longitude=53.82838181057285,
        region=Region.MINSK,
    )

    PINSK = PointSchema(
        label="Пинск",
        latitude=26.111811093605997,
        longitude=52.12223760297976,
        region=Region.BREST,
    )

    VITEBSK = PointSchema(
        label="Витебск",
        latitude=30.250042135934226,
        longitude=55.25257562100984,
        region=Region.VITEBSK,
    )

    LIDA = PointSchema(
        label="Лида",
        latitude=25.32336091231988,
        longitude=53.90227318372977,
        region=Region.GRODNO,
    )

    BARANOVICHI = PointSchema(
        label="Барановичи",
        longitude=53.13190185894763,
        latitude=25.97158074066798,
        region=Region.BREST,
    )

    STOLBTSY = PointSchema(
        label="Столбцы",
        latitude=26.732607935963017,
        longitude=53.46677208676115,
        region=Region.MINSK,
    )

    POLESSKAYA_BOLOTNAYA = PointSchema(
        label="Полесская, болотная",
        latitude=26.667029013394274,
        longitude=52.29983981155924,
        region=Region.BREST,
    )

    DROGICHIN = PointSchema(
        label="Дрогичин",
        latitude=25.0838433995118,
        longitude=52.20004370649066,
        region=Region.BREST,
    )

    GOMEL = PointSchema(
        label="Гомель",
        latitude=30.963081201303428,
        longitude=52.402061468751455,
        region=Region.GOMEL,
    )

    NAROCH_OZERNAYA = PointSchema(
        label="Нарочь, озерная",
        latitude=26.684290791688372,
        longitude=54.899256667266,
        region=Region.VITEBSK,
    )

    VOLOZHIN = PointSchema(
        label="Воложин",
        latitude=26.51694607389268,
        longitude=54.10018849587838,
        region=Region.MINSK,
    )

    VERHNEDVINSK = PointSchema(
        label="Верхнедвинск",
        latitude=27.940101948630605,
        longitude=55.8208765412649,
        region=Region.VITEBSK,
    )

    SENNO = PointSchema(
        label="Сенно",
        latitude=29.687798174910593,
        longitude=54.80456568197694,
        region=Region.VITEBSK,
    )

    GRODNO_AMSG = PointSchema(
        label="Гродно, АМСГ",
        latitude=24.05807929514318,
        longitude=53.60193676812893,
        region=Region.GRODNO,
    )

    MOKRANY = PointSchema(
        label="Мокраны",
        latitude=24.262048260884608,
        longitude=51.83469016263843,
        region=Region.BREST,
    )

    OLTUSH = PointSchema(
        label="Олтуш",
        latitude=23.97093118533709,
        longitude=51.69107406162166,
        region=Region.BREST,
    )

    VERCHNI_TEREBEZHOV = PointSchema(
        label="Верхний Теребежов",
        latitude=26.725999562270026,
        longitude=51.83600602350391,
        region=Region.BREST,
    )

    GLUSHKEVICHI = PointSchema(
        label="Глушкевичи",
        latitude=27.825665051237728,
        longitude=51.61087690551236,
        region=Region.GOMEL,
    )

    SLOVECHNO = PointSchema(
        label="Словечно",
        latitude=29.068442241735667,
        longitude=51.63093077915665,
        region=Region.GOMEL,
    )

    NOVAYA_IOLCHA = PointSchema(
        label="Новая Иолча",
        latitude=30.531611339649682,
        longitude=51.49095727903912,
        region=Region.GOMEL,
    )

    DOMZHERITSY = PointSchema(
        label="Домжерицы",
        latitude=28.349495110191032,
        longitude=54.73569818149728,
        region=Region.VITEBSK,
    )

    def __init__(self, vals: dict):
        self.label = vals["label"]
        self.latitude = vals["latitude"]
        self.longitude = vals["longitude"]
        self.region = vals["region"]

    @property
    def coordinates(self) -> Coordinates:
        return self.latitude, self.longitude


class Emoji(str, enum.Enum):
    HOUSE = emojize("🏡")
    ARROW = emojize("⤵")
    RIGHT_ARROW = emojize("▶")
    LEFT_ARROW = emojize("◀")
    COFFEE = emojize("☕")
    GRAPH = emojize("📈")


class ButtonSchema(TypedDict, total=False):
    """
    Schema for Button.
    """

    label: str
    url: ParseResult
    callback_data: str


class Button(enum.Enum):
    MAIN_MENU = ButtonSchema(label="Главное меню")
    NEXT = ButtonSchema(label=f"{Emoji.RIGHT_ARROW * 2}")
    NEXT_ARROW = ButtonSchema(label=f"{Emoji.RIGHT_ARROW}")
    PREV = ButtonSchema(label=f"{Emoji.LEFT_ARROW * 2}")
    PREV_ARROW = ButtonSchema(label=f"{Emoji.LEFT_ARROW}")
    MONITORING = ButtonSchema(label="Радиационный мониторинг")
    SEND_LOCATION = ButtonSchema(label="Отправить мою геопозицию")
    POINTS = ButtonSchema(label="Пункты наблюдения")
    BREST = ButtonSchema(label=f"{Region.BREST} {Emoji.HOUSE}")
    VITEBSK = ButtonSchema(label=f"{Region.VITEBSK} {Emoji.HOUSE}")
    GOMEL = ButtonSchema(label=f"{Region.GOMEL} {Emoji.HOUSE}")
    GRODNO = ButtonSchema(label=f"{Region.GRODNO} {Emoji.HOUSE}")
    MINSK = ButtonSchema(label=f"{Region.MINSK} {Emoji.HOUSE}")
    MOGILEV = ButtonSchema(label=f"{Region.MOGILEV} {Emoji.HOUSE}")
    HIDE_KEYBOARD = ButtonSchema(label="Скрыть клавиатуру")

    TOTAL_COUNT_USERS = ButtonSchema(
        label="Get total count users",
        callback_data=str(uuid.uuid4()),
    )

    LIST_ADMIN = ButtonSchema(
        label="Get list admin IDs",
        callback_data=str(uuid.uuid4()),
    )

    ADD_ADMIN = ButtonSchema(
        label="Add new admin by user ID",
        callback_data=str(uuid.uuid4()),
    )

    DEL_ADMIN = ButtonSchema(
        label="Delete admin by user ID",
        callback_data=str(uuid.uuid4()),
    )

    SHOW_CHART = ButtonSchema(
        label=f"Показать на графике {Emoji.GRAPH}",
        callback_data=str(uuid.uuid4()),
    )

    DONATE = ButtonSchema(
        label=f"{BotInfo.DONATE} {Emoji.COFFEE}",
        url=urlparse("https://www.buymeacoffee.com/vitalyskopets"),
    )

    def __init__(self, vals: dict) -> None:
        self.label = vals["label"] if vals.get("label") else None
        self.callback_data = (
            vals["callback_data"] if vals.get("callback_data") else None
        )
        self.url = vals["url"].geturl() if vals.get("url") else None


@dataclass(frozen=True)
class Command:
    START: str = "start"
    HELP: str = "help"
    ADMIN: str = "admin"
    DONATE: str = "donate"


class Action(str, enum.Enum):
    START = "start_command"
    HELP = "help_command"
    DONATE = "donate_command"
    ADMIN = "admin_command"
    GET_COUNT = "get_total_count_users"
    GET_LIST = "get_list_of_admin_IDs"
    ADD_ADMIN = "add_admin_by_user_ID"
    GREETING = "sent_greeting_message"
    MESSAGE = "unknown_message"
    MONITORING = "radiation_monitoring"
    LOCATION = "sent_location"
    POINTS = "monitoring_points"
    BREST = "Brest_region"
    VITEBSK = "Vitebsk_region"
    GOMEL = "Gomel_region"
    GRODNO = "Grodno_region"
    MINSK = "Minsk_region"
    MOGILEV = "Mogilev_region"
    MAIN_MENU = "main_menu"
    NEXT = "next"
    PREV = "previosly"
    HIDE_KEYBOARD = "hide_keyboard"
    SHOW_CHART = "show_chart"

    def __str__(self) -> str:
        return self.value
