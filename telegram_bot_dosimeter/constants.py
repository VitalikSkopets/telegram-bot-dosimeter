from dataclasses import dataclass
from enum import Enum
from typing import Sequence

__all__ = (
    "ADMIN_ID",
    "LIST_OF_ADMIN_IDS",
    "MonitoringPoint",
    "MONITORING_POINTS",
    "Brest_region",
    "Vitebsk_region",
    "Grodno_region",
    "Mogilev_region",
    "Minsk_region",
    "Gomel_region",
    "Command",
    "Button",
    "Action",
)

ADMIN_ID: int = 413818791
LIST_OF_ADMIN_IDS: Sequence[int] = (ADMIN_ID,)


@dataclass(slots=True, frozen=True)
class MonitoringPoint:
    name: str
    longitude: float
    latitude: float

    @property
    def coordinates(self) -> tuple[float, float]:
        return self.longitude, self.latitude


MONITORING_POINTS: tuple[MonitoringPoint, ...] = (
    Mogilev := MonitoringPoint(
        name="Могилев",
        longitude=53.69298772769127,
        latitude=30.375068475712993,
    ),
    Mstislavl := MonitoringPoint(
        name="Мстиславль",
        longitude=54.025123497951235,
        latitude=31.742790754635983,
    ),
    Polotsk := MonitoringPoint(
        name="Полоцк",
        longitude=55.47475184602021,
        latitude=28.751296645976183,
    ),
    Sharkovshchina := MonitoringPoint(
        name="Шарковщина",
        longitude=55.36281482842422,
        latitude=27.456996363944278,
    ),
    Minsk := MonitoringPoint(
        name="Минск",
        longitude=53.92751824354786,
        latitude=27.63548838979854,
    ),
    Lyntupy := MonitoringPoint(
        name="Лынтупы",
        longitude=55.04878637860638,
        latitude=26.306634538263953,
    ),
    Visokoe := MonitoringPoint(
        name="Высокое",
        longitude=52.366928433095,
        latitude=23.38374438625246,
    ),
    Pruzhany := MonitoringPoint(
        name="Пружаны",
        longitude=52.567268449727045,
        latitude=24.48545241420398,
    ),
    Slutsk := MonitoringPoint(
        name="Слуцк",
        longitude=53.05284098247522,
        latitude=27.552283199561725,
    ),
    Bragin := MonitoringPoint(
        name="Брагин",
        longitude=51.7969974359342,
        latitude=30.246689891878724,
    ),
    Orsha := MonitoringPoint(
        name="Орша",
        longitude=54.503170699795774,
        latitude=30.443815788156527,
    ),
    Mozyr := MonitoringPoint(
        name="Мозырь",
        longitude=52.036635775856084,
        latitude=29.1925370196736,
    ),
    Slavgorord := MonitoringPoint(
        name="Славгорорд",
        longitude=53.45088516337511,
        latitude=31.003458658160586,
    ),
    Vasilevichi := MonitoringPoint(
        name="Василевичи",
        longitude=52.25207675198943,
        latitude=29.838848231201965,
    ),
    Zhlobin := MonitoringPoint(
        name="Жлобин",
        longitude=52.89414619807851,
        latitude=30.043705893277984,
    ),
    Gorki := MonitoringPoint(
        name="Горки",
        longitude=54.30393502455042,
        latitude=30.94344246329931,
    ),
    Volkovysk := MonitoringPoint(
        name="Волковыск",
        longitude=53.16692103793095,
        latitude=24.448995268762964,
    ),
    Oktyabr := MonitoringPoint(
        name="Октябрь",
        longitude=52.63342658653018,
        latitude=28.883476209528087,
    ),
    Kostyukovichi := MonitoringPoint(
        name="Костюковичи",
        longitude=53.35847386774336,
        latitude=32.070027796122154,
    ),
    Brest := MonitoringPoint(
        name="Брест",
        longitude=52.116580901478635,
        latitude=23.685652135212752,
    ),
    Bobruisk := MonitoringPoint(
        name="Бобруйск",
        longitude=53.20853347538013,
        latitude=29.127272432117724,
    ),
    Ivatsevichi := MonitoringPoint(
        name="Ивацевичи",
        longitude=52.716654759080775,
        latitude=25.350471424000386,
    ),
    Vileyka := MonitoringPoint(
        name="Вилейка",
        longitude=54.48321442087189,
        latitude=26.89989831916185,
    ),
    Borisov := MonitoringPoint(
        name="Борисов",
        longitude=54.26563317790094,
        latitude=28.49760585109516,
    ),
    Zhitkovichi := MonitoringPoint(
        name="Житковичи",
        longitude=52.21411222651425,
        latitude=27.870082634924596,
    ),
    Oshmyany := MonitoringPoint(
        name="Ошмяны",
        longitude=54.43300284193779,
        latitude=25.935350063150867,
    ),
    Berezino := MonitoringPoint(
        name="Березино",
        longitude=53.82838181057285,
        latitude=28.99727106523084,
    ),
    Pinsk := MonitoringPoint(
        name="Пинск",
        longitude=52.12223760297976,
        latitude=26.111811093605997,
    ),
    Vitebsk := MonitoringPoint(
        name="Витебск",
        longitude=55.25257562100984,
        latitude=30.250042135934226,
    ),
    Lida := MonitoringPoint(
        name="Лида",
        longitude=53.90227318372977,
        latitude=25.32336091231988,
    ),
    Baranovichi := MonitoringPoint(
        name="Барановичи",
        longitude=53.13190185894763,
        latitude=25.97158074066798,
    ),
    Stolbtsy := MonitoringPoint(
        name="Столбцы",
        longitude=53.46677208676115,
        latitude=26.732607935963017,
    ),
    Polesskaya_bolotnaya := MonitoringPoint(
        name="Полесская, болотная",
        longitude=52.29983981155924,
        latitude=26.667029013394274,
    ),
    Drogichin := MonitoringPoint(
        name="Дрогичин",
        longitude=52.20004370649066,
        latitude=25.0838433995118,
    ),
    Gomel := MonitoringPoint(
        name="Гомель",
        longitude=52.402061468751455,
        latitude=30.963081201303428,
    ),
    Naroch_ozernaya := MonitoringPoint(
        name="Нарочь, озерная",
        longitude=54.899256667266,
        latitude=26.684290791688372,
    ),
    Volozhin := MonitoringPoint(
        name="Воложин",
        longitude=54.10018849587838,
        latitude=26.51694607389268,
    ),
    Verhnedvinsk := MonitoringPoint(
        name="Верхнедвинск",
        longitude=55.8208765412649,
        latitude=27.940101948630605,
    ),
    Senno := MonitoringPoint(
        name="Сенно",
        longitude=54.80456568197694,
        latitude=29.687798174910593,
    ),
    Grodno_AMSG := MonitoringPoint(
        name="Гродно, АМСГ",
        longitude=53.60193676812893,
        latitude=24.05807929514318,
    ),
    Mokrany := MonitoringPoint(
        name="Мокраны",
        longitude=51.83469016263843,
        latitude=24.262048260884608,
    ),
    Oltush := MonitoringPoint(
        name="Олтуш",
        longitude=51.69107406162166,
        latitude=23.97093118533709,
    ),
    Verchni_Terebezhov := MonitoringPoint(
        name="Верхний Теребежов",
        longitude=51.83600602350391,
        latitude=26.725999562270026,
    ),
    Glushkevichi := MonitoringPoint(
        name="Глушкевичи",
        longitude=51.61087690551236,
        latitude=27.825665051237728,
    ),
    Slovechno := MonitoringPoint(
        name="Словечно",
        longitude=51.63093077915665,
        latitude=29.068442241735667,
    ),
    Novaya_Iolcha := MonitoringPoint(
        name="Новая Иолча",
        longitude=51.49095727903912,
        latitude=30.531611339649682,
    ),
    Domzheritsy := MonitoringPoint(
        name="Домжерицы",
        longitude=54.73569818149728,
        latitude=28.349495110191032,
    ),
)


@dataclass(slots=True, frozen=True)
class Region:
    name: str
    monitoring_points: tuple[MonitoringPoint, ...]


Brest_region = Region(
    name="Брестская область",
    monitoring_points=(
        Visokoe,
        Pruzhany,
        Brest,
        Ivatsevichi,
        Pinsk,
        Baranovichi,
        Polesskaya_bolotnaya,
        Drogichin,
        Mokrany,
        Oltush,
        Verchni_Terebezhov,
    ),
)

Vitebsk_region = Region(
    name="Витебская область",
    monitoring_points=(
        Polotsk,
        Sharkovshchina,
        Lyntupy,
        Orsha,
        Vitebsk,
        Naroch_ozernaya,
        Verhnedvinsk,
        Senno,
        Domzheritsy,
    ),
)

Grodno_region = Region(
    name="Гродненская область",
    monitoring_points=(
        Volkovysk,
        Oshmyany,
        Lida,
        Grodno_AMSG,
    ),
)

Mogilev_region = Region(
    name="Могилевская область",
    monitoring_points=(
        Mogilev,
        Mstislavl,
        Slavgorord,
        Gorki,
        Kostyukovichi,
        Bobruisk,
    ),
)

Minsk_region = Region(
    name="Минск и Минская область",
    monitoring_points=(
        Minsk,
        Slutsk,
        Vileyka,
        Borisov,
        Berezino,
        Stolbtsy,
        Volozhin,
    ),
)

Gomel_region = Region(
    name="Гомельская область",
    monitoring_points=(
        Bragin,
        Mozyr,
        Vasilevichi,
        Zhlobin,
        Oktyabr,
        Zhitkovichi,
        Gomel,
        Glushkevichi,
        Slovechno,
    ),
)


class Command(str, Enum):
    START = "start"
    HELP = "help"


class Button(str, Enum):
    MAIN_MENU = "Главное меню"
    MONITORING = "Радиационный мониторинг"
    SEND_LOCATION = "Отправить мою геопозицию"
    POINTS = "Пункты наблюдения"
    BREST = Brest_region.name
    VITEBSK = Vitebsk_region.name
    GOMEL = Gomel_region.name
    GRODNO = Grodno_region.name
    MINSK = Minsk_region.name
    MOGILEV = Mogilev_region.name


class Action(str, Enum):
    START = "Start command"
    HELP = "Help command"
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
