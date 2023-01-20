import enum
import uuid
from dataclasses import dataclass
from pathlib import Path

from emoji.core import emojize

from dosimeter.config import BASE_DIR

__all__ = (
    "ADMIN_ID",
    "LIST_OF_ADMIN_IDS",
    "TEMP_LIST_OF_ADMIN_IDS",
    "Action",
    "Buttons",
    "Command",
    "Emoji",
    "Files",
    "Points",
    "Regions",
)

ADMIN_ID: int = 413818791 or 1120930631
LIST_OF_ADMIN_IDS: tuple[int, int] = (ADMIN_ID, 487236325)
TEMP_LIST_OF_ADMIN_IDS: list[int] = []


@dataclass(frozen=True)
class Files:
    SECRET_KEY: Path = BASE_DIR / "secret.pem"
    PUBLIC_KEY: Path = BASE_DIR / "public.pem"


@dataclass(frozen=True)
class Regions:
    BREST: str = "Брестская область"
    VITEBSK: str = "Витебская область"
    GOMEL: str = "Гомельская область"
    GRODNO: str = "Гродненская область"
    MOGILEV: str = "Могилевская область"
    MINSK: str = "Минск и Минская область"


class Points(enum.Enum):
    MOGILEV = {
        "label": "Могилев",
        "longitude": 53.69298772769127,
        "latitude": 30.375068475712993,
        "region": Regions.MOGILEV,
    }

    MSTISLAVL = {
        "label": "Мстиславль",
        "longitude": 54.025123497951235,
        "latitude": 31.742790754635983,
        "region": Regions.MOGILEV,
    }

    POLOTSK = {
        "label": "Полоцк",
        "longitude": 55.47475184602021,
        "latitude": 28.751296645976183,
        "region": Regions.VITEBSK,
    }

    SHARKOVSHCHINA = {
        "label": "Шарковщина",
        "longitude": 55.36281482842422,
        "latitude": 27.456996363944278,
        "region": Regions.VITEBSK,
    }

    MINSK = {
        "label": "Минск",
        "longitude": 53.92751824354786,
        "latitude": 27.63548838979854,
        "region": Regions.MINSK,
    }

    LYNTUPY = {
        "label": "Лынтупы",
        "longitude": 55.04878637860638,
        "latitude": 26.306634538263953,
        "region": Regions.VITEBSK,
    }

    VISOKOE = {
        "label": "Высокое",
        "longitude": 52.366928433095,
        "latitude": 23.38374438625246,
        "region": Regions.BREST,
    }

    PRUZHANY = {
        "label": "Пружаны",
        "longitude": 52.567268449727045,
        "latitude": 24.48545241420398,
        "region": Regions.BREST,
    }

    SLUTSK = {
        "label": "Слуцк",
        "longitude": 53.05284098247522,
        "latitude": 27.552283199561725,
        "region": Regions.MINSK,
    }

    BRAGIN = {
        "label": "Брагин",
        "longitude": 51.7969974359342,
        "latitude": 30.246689891878724,
        "region": Regions.GOMEL,
    }

    ORSHA = {
        "label": "Орша",
        "longitude": 54.503170699795774,
        "latitude": 30.443815788156527,
        "region": Regions.VITEBSK,
    }

    MOZYR = {
        "label": "Мозырь",
        "longitude": 52.036635775856084,
        "latitude": 29.1925370196736,
        "region": Regions.GOMEL,
    }

    SLAVGORORD = {
        "label": "Славгорорд",
        "longitude": 53.45088516337511,
        "latitude": 31.003458658160586,
        "region": Regions.MOGILEV,
    }

    VASILEVICHI = {
        "label": "Василевичи",
        "longitude": 52.25207675198943,
        "latitude": 29.838848231201965,
        "region": Regions.GOMEL,
    }

    ZHLOBIN = {
        "label": "Жлобин",
        "longitude": 52.89414619807851,
        "latitude": 30.043705893277984,
        "region": Regions.GOMEL,
    }

    GORKI = {
        "label": "Горки",
        "longitude": 54.30393502455042,
        "latitude": 30.94344246329931,
        "region": Regions.MOGILEV,
    }

    VOLKOVYSK = {
        "label": "Волковыск",
        "longitude": 53.16692103793095,
        "latitude": 24.448995268762964,
        "region": Regions.GRODNO,
    }

    OKTYABR = {
        "label": "Октябрь",
        "longitude": 52.63342658653018,
        "latitude": 28.883476209528087,
        "region": Regions.GOMEL,
    }

    KOSTYUKOVICHI = {
        "label": "Костюковичи",
        "longitude": 53.35847386774336,
        "latitude": 32.070027796122154,
        "region": Regions.MOGILEV,
    }

    BREST = {
        "label": "Брест",
        "longitude": 52.116580901478635,
        "latitude": 23.685652135212752,
        "region": Regions.BREST,
    }

    BOBRUISK = {
        "label": "Бобруйск",
        "longitude": 53.20853347538013,
        "latitude": 29.127272432117724,
        "region": Regions.MOGILEV,
    }

    IVATSEVICHI = {
        "label": "Ивацевичи",
        "longitude": 52.716654759080775,
        "latitude": 25.350471424000386,
        "region": Regions.BREST,
    }

    VILEYKA = {
        "label": "Вилейка",
        "longitude": 54.48321442087189,
        "latitude": 26.89989831916185,
        "region": Regions.MINSK,
    }

    BORISOV = {
        "label": "Борисов",
        "longitude": 54.26563317790094,
        "latitude": 28.49760585109516,
        "region": Regions.MINSK,
    }

    ZHITKOVICHI = {
        "label": "Житковичи",
        "longitude": 52.21411222651425,
        "latitude": 27.870082634924596,
        "region": Regions.GOMEL,
    }

    OSHMYANY = {
        "label": "Ошмяны",
        "longitude": 54.43300284193779,
        "latitude": 25.935350063150867,
        "region": Regions.GRODNO,
    }

    BEREZINO = {
        "label": "Березино",
        "longitude": 53.82838181057285,
        "latitude": 28.99727106523084,
        "region": Regions.MINSK,
    }

    PINSK = {
        "label": "Пинск",
        "longitude": 52.12223760297976,
        "latitude": 26.111811093605997,
        "region": Regions.BREST,
    }

    VITEBSK = {
        "label": "Витебск",
        "longitude": 55.25257562100984,
        "latitude": 30.250042135934226,
        "region": Regions.VITEBSK,
    }

    LIDA = {
        "label": "Лида",
        "longitude": 53.90227318372977,
        "latitude": 25.32336091231988,
        "region": Regions.GRODNO,
    }

    BARANOVICHI = {
        "label": "Барановичи",
        "longitude": 53.13190185894763,
        "latitude": 25.97158074066798,
        "region": Regions.BREST,
    }

    STOLBTSY = {
        "label": "Столбцы",
        "longitude": 53.46677208676115,
        "latitude": 26.732607935963017,
        "region": Regions.MINSK,
    }

    POLESSKAYA_BOLOTNAYA = {
        "label": "Полесская, болотная",
        "longitude": 52.29983981155924,
        "latitude": 26.667029013394274,
        "region": Regions.BREST,
    }

    DROGICHIN = {
        "label": "Дрогичин",
        "longitude": 52.20004370649066,
        "latitude": 25.0838433995118,
        "region": Regions.BREST,
    }

    GOMEL = {
        "label": "Гомель",
        "longitude": 52.402061468751455,
        "latitude": 30.963081201303428,
        "region": Regions.GOMEL,
    }

    NAROCH_OZERNAYA = {
        "label": "Нарочь, озерная",
        "longitude": 54.899256667266,
        "latitude": 26.684290791688372,
        "region": Regions.VITEBSK,
    }

    VOLOZHIN = {
        "label": "Воложин",
        "longitude": 54.10018849587838,
        "latitude": 26.51694607389268,
        "region": Regions.MINSK,
    }

    VERHNEDVINSK = {
        "label": "Верхнедвинск",
        "longitude": 55.8208765412649,
        "latitude": 27.940101948630605,
        "region": Regions.VITEBSK,
    }

    SENNO = {
        "label": "Сенно",
        "longitude": 54.80456568197694,
        "latitude": 29.687798174910593,
        "region": Regions.VITEBSK,
    }

    GRODNO_AMSG = {
        "label": "Гродно, АМСГ",
        "longitude": 53.60193676812893,
        "latitude": 24.05807929514318,
        "region": Regions.GRODNO,
    }

    MOKRANY = {
        "label": "Мокраны",
        "longitude": 51.83469016263843,
        "latitude": 24.262048260884608,
        "region": Regions.BREST,
    }

    OLTUSH = {
        "label": "Олтуш",
        "longitude": 51.69107406162166,
        "latitude": 23.97093118533709,
        "region": Regions.BREST,
    }

    VERCHNI_TEREBEZHOV = {
        "label": "Верхний Теребежов",
        "longitude": 51.83600602350391,
        "latitude": 26.725999562270026,
        "region": Regions.BREST,
    }

    GLUSHKEVICHI = {
        "label": "Глушкевичи",
        "longitude": 51.61087690551236,
        "latitude": 27.825665051237728,
        "region": Regions.GOMEL,
    }

    SLOVECHNO = {
        "label": "Словечно",
        "longitude": 51.63093077915665,
        "latitude": 29.068442241735667,
        "region": Regions.GOMEL,
    }

    NOVAYA_IOLCHA = {
        "label": "Новая Иолча",
        "longitude": 51.49095727903912,
        "latitude": 30.531611339649682,
        "region": Regions.GOMEL,
    }

    DOMZHERITSY = {
        "label": "Домжерицы",
        "longitude": 54.73569818149728,
        "latitude": 28.349495110191032,
        "region": Regions.VITEBSK,
    }

    def __init__(self, vals: dict):
        self.label = vals["label"]
        self.longitude = vals["longitude"]
        self.latitude = vals["latitude"]
        self.region = vals["region"]

    @property
    def coordinates(self) -> tuple[float, float]:
        return self.longitude, self.latitude


class Emoji(str, enum.Enum):
    RADIO = emojize("☢️")
    ROBOT = emojize("🤖")
    HOUSE = emojize("🏡")
    SOS = emojize("🆘")
    ARROW = emojize("⤵")
    RIGHT_ARROW = emojize("▶")
    LEFT_ARROW = emojize("◀")
    KEYBOARD = emojize("⌨️")


class Buttons(enum.Enum):

    MAIN_MENU = {
        "label": "Главное меню",
        "callback_data": str(uuid.uuid4()),
    }
    NEXT = {
        "label": f"{Emoji.RIGHT_ARROW * 2}",
        "callback_data": str(uuid.uuid4()),
    }
    NEXT_ARROW = {
        "label": f"{Emoji.RIGHT_ARROW}",
        "callback_data": str(uuid.uuid4()),
    }
    PREV = {
        "label": f"{Emoji.LEFT_ARROW * 2}",
        "callback_data": str(uuid.uuid4()),
    }
    PREV_ARROW = {
        "label": f"{Emoji.LEFT_ARROW}",
        "callback_data": str(uuid.uuid4()),
    }
    MONITORING = {
        "label": "Радиационный мониторинг",
        "callback_data": str(uuid.uuid4()),
    }
    SEND_LOCATION = {
        "label": "Отправить мою геопозицию",
        "callback_data": str(uuid.uuid4()),
    }
    POINTS = {
        "label": "Пункты наблюдения",
        "callback_data": str(uuid.uuid4()),
    }
    BREST = {
        "label": f"{Regions.BREST} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    VITEBSK = {
        "label": f"{Regions.VITEBSK} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    GOMEL = {
        "label": f"{Regions.GOMEL} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    GRODNO = {
        "label": f"{Regions.GRODNO} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    MINSK = {
        "label": f"{Regions.MINSK} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    MOGILEV = {
        "label": f"{Regions.MOGILEV} {Emoji.HOUSE}",
        "callback_data": str(uuid.uuid4()),
    }
    HIDE_KEYBOARD = {
        "label": "Скрыть клавиатуру",
        "callback_data": str(uuid.uuid4()),
    }
    TOTAL_COUNT_USERS = {
        "label": "Get total count users",
        "callback_data": str(uuid.uuid4()),
    }
    LIST_ADMIN = {
        "label": "Get list admin IDs",
        "callback_data": str(uuid.uuid4()),
    }
    ADD_ADMIN = {
        "label": "Add new admin by user ID",
        "callback_data": str(uuid.uuid4()),
    }
    DEL_ADMIN = {
        "label": "Delete admin by user ID",
        "callback_data": str(uuid.uuid4()),
    }

    def __init__(self, vals: dict) -> None:
        self.label = vals["label"]
        self.callback_data = vals["callback_data"]


@dataclass(frozen=True)
class Command:
    START: str = "start"
    HELP: str = "help"
    ADMIN: str = "admin"


class Action(str, enum.Enum):
    START = "Start command"
    HELP = "Help command"
    ADMIN = "Admin command"
    GET_COUNT = "Get total count users"
    GET_LIST = "Get list of admin IDs"
    ADD_ADMIN = "Add admin by user ID"
    GREETING = "Greeting message"
    MESSAGE = "Unknown message"
    MONITORING = "Radiation monitoring"
    LOCATION = "Send geolocation"
    POINTS = "Monitoring points"
    BREST = "Brest region"
    VITEBSK = "Vitebsk region"
    GOMEL = "Gomel region"
    GRODNO = "Grodno region"
    MINSK = "Minsk region"
    MOGILEV = "Mogilev region"
    MAIN_MENU = "Main menu"
    NEXT = "Next"
    PREV = "Previosly"
    HIDE_KEYBOARD = "Hide keyboard"


@dataclass(frozen=True)
class Description:
    BOT: str = """
    Этот бот может информировать пользователя по состоянию на текущую дату о
    радиационной обстановке в Беларуси и об уровне мощности эквивалентной дозы
    гамма-излучения, зафиксированного в сети радиационного мониторинга Министерства
    природных ресурсов и охраны окружающей среды Беларуси. Источник: ©rad.org.by
    Разработано: ©itrexgroup.com
    """
    START: str = "Launch this bot / Запустить этого бота"
    HELP: str = "Useful information about this bot / Полезная информация об этом боте"
    ADMIN: str = "List of admin commands (limited access)"
