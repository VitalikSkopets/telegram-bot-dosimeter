from typing import Final
from bs4 import BeautifulSoup
import requests
from emoji.core import emojize
from fake_useragent import UserAgent
from datetime import datetime
import locale
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from config import URL1

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
    'help': f'{smile1} Бот-дозиметр может информировать пользователя по состоянию на <i>текущую дату</i> о радиационной '
            f'обстановке в Беларуси и об уровне мощности дозы (далее - МД) гамма-излучения, зафиксированного '
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
    response = requests.get(url, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def scraper(update, region: list[str]) -> None:
    """
    Функция вызывает метод get_html(), который отправляет get-запрос и скрайпит html-структуру веб-ресурса
    https://rad.org.by/radiation.xml. Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в соответстсвующей области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param region: список элементами которого являются значения (названия пунктов наблюдения) ключей (названия областей)
    из словаря ADMINISTRATIVE_DIVISION в модуле config.py
    :return: None
    """
    user = update.effective_user
    try:
        points, indications = get_html().find_all('title'), get_html().find_all('rad')
        points.reverse()
        indications.reverse()
        zipped_values = zip(points, indications)
        zipped_list = list(zipped_values)
        update.message.reply_text(f'| *Пункт наблюдения* | *Дата и время* | *МД гамма-излучения* |',
                                  parse_mode=ParseMode.MARKDOWN)
        for i in range(0, len(zipped_list)):
            if points[i].text in region:
                update.message.reply_text(f'| "*{points[i].text}*" | _{today}_ | *{indications[i].text}* мкЗв/ч |',
                                          parse_mode=ParseMode.MARKDOWN)
    except Exception:
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


def encryption(TOKEN_FOR_DB, line: str) -> str:
    """
    Функция симетричного шифрования строковых данных first_name, last_name и username пользователя для последующей
    передачи шифрованных данных в базу данных для долговременного хранения
    :param TOKEN_FOR_DB: сгенерированный ключ-пароль для шифрования
    :param line: строковый объект шифрования
    :return: строковый объект - зашифрованные first_name и(или) last_name, username
    """
    if line is not None:
        cryptoline = TOKEN_FOR_DB.encrypt(line.encode('utf-8'))
        return cryptoline.decode('utf-8')
