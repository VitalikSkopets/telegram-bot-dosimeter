from enum import Enum

from emoji.core import emojize

from telegram_bot_dosimeter.constants import Button

__all__ = (
    "Emoji",
    "Message",
)


class Emoji(Enum):
    RADIO = emojize(":radioactive_sign:", use_aliases=True)
    ROBOT = emojize(":robot_face:", use_aliases=True)
    SOS = emojize(":SOS_button:", use_aliases=True)
    ARROW = emojize(":right_arrow_curving_down:", use_aliases=True)


class Message(str, Enum):
    DESCRIPTION = f"по состоянию на <i>текущую дату</i> уровень мощности эквивалентной дозы гамма-излучения, зафиксированного на <i>ближайшем</i> пункте наблюдения, нажми <b>{Button.SEND_LOCATION}</b>.\n\nЧтобы узнать обстановку в сети радиационного мониторинга Беларуси, нажми <b>{Button.MONITORING}</b>.\n\nЧтобы узнать сводку пунктов наблюдения в сети радиационного мониторинга, нажми <b>{Button.POINTS}</b> и выбери интересующий регион."
    START = f"\nЯ бот-дозиметр {Emoji.RADIO.value}\n\nЧтобы узнать {DESCRIPTION}"
    HELP = "Бот-дозиметр может информировать пользователя по состоянию на <i>текущую дату</i> о радиационной обстановке в Беларуси и об уровне мощности дозы (далее - МД) гамма-излучения, зафиксированного на <i>ближайшем</i> к пользователю пункте наблюдения сети радиационного мониторинга Министерства природных ресурсов и охраны окружающей среды Беларуси (далее - Министерства).\n\nВ соответствии с приказом Министерства от 30.04.2021 №151-ОД, измерение уровней МД гамма-излучения проводится ежедневно в 06:00 часов по Гринвичскому времени дозиметрами или другими средствами измерения со статической погрешностью не более 20%.\n\nДля оценки воздействия на организм человека используется понятие мощности эквивалентной дозы, которая измеряется в Зивертах/час.\n\nВ быту можно считать, что 1 Зиверт = 100 Рентген.\n\n<i>Безопасным</i> считается уровень радиации, приблизительно <b>до 0.5 мкЗв/ч</b>."
    GREET = f"\nЯ могу сообщать тебе информацию {DESCRIPTION}"
    LOCATION = "<i>{}</i> до ближайшего пункта наблюдения <b>{}</b>.\n\nВ пункте наблюдения <b>{}</b> по состоянию на <i>{}</i> уровень эквивалентной дозы радиации составляет <b>{}</b> мкЗв/ч."
    INFO = f"в настоящее время актуальная информация о состоянии радиационной обстановки недоступна. Попробуй спросить {Emoji.ROBOT.value} в другой раз и обязательно получишь ответ!"
    UNKNOWN = f"Ничего не понятно, но Оoоочень интересно {Emoji.ROBOT.value}\nПопробуй команду /help."
    MONITORING = "По состоянию на текущую дату радиационная обстановка на территории Республики Беларусь стабильная, мощность дозы гамма-излучения (МД) на пунктах наблюдений радиационного мониторинга атмосферного воздуха соответствует установившимся многолетним значениям. Как и прежде, повышенный уровень МД гамма-излучения зарегистрирован в пункте наблюдения города Брагин, находящегося в зоне радиоактивного загрязнения, обусловленного катастрофой на Чернобыльской АЭС."
    AVG = "\n\n<b>Среднее</b> значение уровня МД гамма-излучения в сети региоанльных пунктов радиационного мониторинга Министерства природных ресурсов и охраны окружающей среды Беларуси составляет <b>{:.1f}</b> мкЗв/ч. "
    TABLE = "По состоянию на <i>{}</i>\n\n|<code>{:^20}</code>|<code>{:^13}</code>|\n"
    MEET = "Рад нашему знакомству, <b>{}</b>!{}"
    RADIATION = "Сегодня <i>{}</i> {}\n\nПо стране <i>среднее</i> значение уровня МД гамма-излучения в сети пунктов радиационного мониторинга Министерства природных ресурсов и охраны окружающей среды Беларуси по состоянию на сегодняшний день составляет <b>{:.2f}</b> мкЗв/ч."
    REGION = f"Выбери интересующий регион {Emoji.ARROW.value}"
    ADMIN = f"Выбери команду {Emoji.ARROW.value}"
