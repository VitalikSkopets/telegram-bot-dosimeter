from typing import Final
from bs4 import BeautifulSoup
import requests
from loguru import logger
from emoji.core import emojize
from fake_useragent import UserAgent
from datetime import datetime
import locale
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from config import URL1, SECRET_KEY

locale.setlocale(category=locale.LC_ALL, locale="Russian")
today: Final = datetime.now().strftime("%a %d-%b-%Y %H:%M")

commands = {'start': 'Start using this bot',
            'help': 'Useful information about this bot'
            }

smile1: Final = emojize(':radioactive_sign:', use_aliases=True)
smile2: Final = emojize(':robot_face:', use_aliases=True)

text_messages: Final = {
    'start': f'\n\nЯ бот-дозиметр {smile1} '
             f'\n\nЧтобы узнать по состоянию на <i>текущую дату</i> уровень мощности эквивалентной дозы '
             f'гамма-излучения, зафиксированного на <i>ближайшем</i> пункте наблюдения, '
             f'нажми <b>"Отправить мою геопозицию"</b>.\n\nЧтобы узнать радиационную обстановку в Беларуси, '
             f'нажми <b>"Радиационный мониторинг"</b>.\n\nЧтобы узнать сводку пунктов наблюдения, '
             f'нажми <b>"Пункты наблюдения"</b>.',
    'help': f'{smile1} Бот-дозиметр может информировать пользователя по состоянию на <i>текущую дату</i> о радиационной'
            f' обстановке в Беларуси и об уровне мощности дозы (далее - МД) гамма-излучения, зафиксированного '
            f'на <i>ближайшем</i> к пользователю пункте наблюдения сети радиационного мониторинга Министерства '
            f'природных ресурсов и охраны окружающей среды Беларуси (далее - Министерства). \n\nВ соответствии '
            f'с приказом Министерства от 18.04.2014 №230-ОД, измерение уровней МД гамма-излучения проводится ежедневно '
            f'в 06:00 часов по Гринвичскому времени дозиметрами или другими средствами измерения со статической '
            f'погрешностью не более 20%. \n\nДля оценки воздействия на организм человека используется понятие мощности '
            f'эквивалентной дозы, которая измеряется в Зивертах/час.\n'
            f'\nВ быту можно считать, что 1 Зиверт = 100 Рентген.\n'
            f'\n<i>Безопасным</i> считается уровень радиации, приблизительно <b>до 0.5 мкЗв/ч</b>.',
    'greet': f'\nЯ могу сообщать тебе информацию по состоянию на <i>текущую дату</i> о об уровне мощности эквивалентной'
             f' дозы (МД) гамма-излучения, зафиксированного на <i>ближайшем</i> пункте наблюдения в сети радиационного '
             f'мониторинга. Для этого нажми <b>"Отправить мою геопозицию"</b>.'
             f'\n\nЧтобы узнать радиационную обстановку в Беларуси, нажми <b>"Радиационный мониторинг"</b>.'
             f'\n\nЧтобы узнать сводку пунктов наблюдения, нажми <b>"Пункты наблюдения"</b>.',
    'button1': 'Отправить мою геопозицию',
    'button2': 'Радиационный мониторинг',
    'unknown': f'Ничего не понятно, но очень интересно {smile2}\nПопробуй команду /help.'
}

greeting: Final = ['hello', 'hi', 'hey', 'привет', 'салют', 'здарова', 'здравствуй', 'здравствуйте', 'добрый день',
                   'добрый вечер', 'доброе утро', 'доброго дня', 'хелоу', 'бонжур', 'привестствую', 'здрасте',
                   'какая встреча', 'рад встрече', 'хай', 'здравия желаю', 'приветик', 'доброго времени суток',
                   'здорова', 'здорово', 'мое почтение', 'приветствую тебя', 'сердечно приветствую', 'how are you',
                   'what’s up', 'whats up', 'hello there', 'howdy', 'hiya', 'yo', 'how do you do', 'good morning',
                   'good afternoon', 'good evening', 'peek-a-boo', 'peek a boo', 'hi mister', 'ahoy'
                   ]


def get_html(url=URL1):
    """
    Функия отправляет get-звапрос и скрайпит https://rad.org.by/radiation.xml
    :param url: строквый объект 'https://rad.org.by/radiation.xml'
    :return: объект класса bs4.BeautifulSoup - html-разметка веб-ресурса https://rad.org.by/radiation.xml
    """
    try:
        response = requests.get(url, headers={'User-Agent': UserAgent().random})
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception:
        logger.warning('ERROR while performing the get_html() function')


def format_string(string: str, min_length: int = 20) -> str:
    """
    Функция увеличивает длину строкового объекта до 20 символов заполняя "-" пробельные символы
    :param string: строковый объект - название пункта наблюдения в сети радиационного мониторинга
    :param min_length: длина строкового объекта по умолчанию 20 симовлов
    :return: строковый объект (название пункта наблюдения) длиной 20 символов
    """
    while len(string) < min_length:
        string += "-"
    return string


def scraper(update, region: list[str]) -> None:
    """
    Функция вызывает метод get_html(), который отправляет get-запрос и скрайпит html-структуру веб-ресурса
    https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в соответстсвующей области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю. Также, функция расчитывает среднее арифметическое значение уровня радиации в сети
    соответствующих региоанльных пунктов радиационного мониторинга
    :param update: словарь Update с информацией о пользователе Telegram
    :param region: список элементами которого являются значения (названия пунктов наблюдения) ключей (названия областей)
    из словаря ADMINISTRATIVE_DIVISION в модуле config.py
    :return: None
    """
    user = update.effective_user
    indications_region, table = [], []
    try:
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        for i in range(0, len(zipped_list)):
            if points[i].text in region:
                indications_region.append(float(indications[i].text))
                new_point = format_string(points[i].text)
                table.append('|`{}`|`{:^13}`|'.format(new_point, indications[i].text + ' мкЗв/ч'))
        avg_indication_region = sum(indications_region) / len(indications_region)
        update.message.reply_text('По состоянию на _{}_\n\n|`{:^20}`|`{:^13}`|\n'.format(today, 'Пункт наблюдения',
                                  'Мощность дозы') + '\n'.join(table) + '\n\n*Среднее* значение уровня МД '
                                  'гамма-излучения в сети региоанльных пунктов радиационного мониторинга Министерства '
                                  'природных ресурсов и охраны окружающей среды Беларуси составляет *{:.1f}* мкЗв/ч.'
                                  .format(avg_indication_region), parse_mode=ParseMode.MARKDOWN
                                  )
    except Exception:
        logger.warning('ERROR while performing the scraper() function')
        update.message.reply_text(f"К сожалению, <b>{user['first_name']}</b>, в настоящее время актуальная "
                                  f"информация по интересующему региону отсутствует {smile2}",
                                  parse_mode=ParseMode.HTML
                                  )


def main_keyboard():
    """
    Функция возвращате пользовтелю кнопки меню вместо стандартной клавиатуры
    :return: class ReplyKeyboardMarkup из библиотеки telegram
    """
    return ReplyKeyboardMarkup([['Радиационный мониторинг'],
                                ['Пункты наблюдения'],
                                [KeyboardButton('Отправить мою геопозицию',
                                                request_location=True)]], resize_keyboard=True)


def encrypt(line, key=SECRET_KEY):
    """
    Функция симетричного шифрования строковых объектов - идентификацуионных данных пользователей, хранящихся
    в коллекции users базы данных MongoDB Atlas в полях с ключами first_name, last_name и username
    :param key: сгенерированный ключ шифрования/дешифрования
    :param line: строковый объект - текст полей с ключами first_name и(или) last_name, username коллекции users
    базы данных MongoDB Atlas, подлежащий шифрованию
    :return строковый объект - шифрованый текст полей с ключами first_name и(или) last_name, username коллекции users
    базы данных MongoDB Atlas
    """
    if line is not None:
        try:
            token = key.encrypt(line.encode())
            return token.decode()
        except Exception:
            logger.warning('ERROR while performing the encrypt() function')
