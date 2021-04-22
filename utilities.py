from bs4 import BeautifulSoup
import requests
from emoji.core import emojize
from fake_useragent import UserAgent
from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import URL1


commands = {'start': 'Start using this bot',
            'help': 'Useful information about this bot'
            }

smile = emojize(':radioactive_sign:', use_aliases=True)

text_messages = {
    'start': f'\n\nЯ бот-дозиметр {smile} '
             f'\n\nЧтобы узнать по состоянию на текущую дату уровень мощности эквивалентной дозы гамма-излучения, '
             f'зафиксированного на ближайшем пункте наблюдения, нажми <b>"Отправить мою геопозицию"</b>.'
             f'\n\nЧтобы узнать радиационную обстановку в Беларуси, нажми <b>"Радиационный мониторинг"</b>.'
             f'\n\nЧтобы узнать сводку пунктов наблюдения, нажми <b>"Пункты наблюдения"</b>.',
    'help': f'{smile} Бот-дозиметр может информировать пользователя по состоянию на текущую дату о радиационной '
            f'обстановке в Беларуси и об уровне мощности дозы (далее - МД) гамма-излучения, зафиксированного '
            f'на ближайшем к пользователю пункте наблюдения сети радиационного мониторинга Министерства природных '
            f'ресурсов и охраны окружающей среды Беларуси (далее - Министерства). \n\nВ соответствии с приказом '
            f'Министерства от 18.04.2014 №230-ОД, измерение уровней МД гамма-излучения проводится ежедневно '
            f'в 06:00 часов по Гринвичскому времени дозиметрами или другими средствами измерения со статической '
            f'погрешностью не более 20%. \n\nДля оценки воздействия на организм человека используется понятие мощности '
            f'эквивалентной дозы, которая измеряется в Зивертах/час.\n'
            f'\nВ быту можно считать, что 1 Зиверт = 100 Рентген.\n'
            f'\n<i>Безопасным</i> считается уровень радиации, приблизительно <b>до 0.5 мкЗв/ч</b>.',
    'greet': f'\nЯ могу сообщать тебе информацию по состоянию на текущую дату о об уровне мощности эквивалентной '
             f'дозы (МД) гамма-излучения, зафиксированного на ближайшем пункте наблюдения в сети радиационного '
             f'мониторинга. Для этого нажми <b>"Отправить мою геопозицию"</b>.'
             f'\n\nЧтобы узнать радиационную обстановку в Беларуси, нажми <b>"Радиационный мониторинг"</b>.'
             f'\n\nЧтобы узнать сводку пунктов наблюдения, нажми <b>"Пункты наблюдения"</b>.',
    'button1': 'Отправить мою геопозицию',
    'button2': 'Радиационный мониторинг',
    'unknown': 'Ничего не понятно, но очень интересно.\nПопробуй команду /help.'
}


def avg_rad():
    """
    Функция скрайпит с ресурса https://rad.org.by/radiation.xml значения радиации во всех пунктах наблюдения
    и расчитывает среднее арефметическое значение уровня радиации в Беларуси
    :return: интерполированная строка со средним значеним величины уровня радиации в формате float
    """
    indications = get_html().find_all('rad')
    avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
    return f' {avg_indication:.2f} мкЗв/ч'


def get_html(url=URL1):
    """
    Функия скрайпинга веб-ресурса https://rad.org.by/radiation.xml
    :param url: строквый объект 'https://rad.org.by/radiation.xml'
    :return: html- разметка веб-ресурса https://rad.org.by/radiation.xml в виде текста
    """
    response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def main_keyboard():
    """
    Функция возвращате пользовтелю кнопки меню вместо стандартной клавиатуры
    :return: class ReplyKeyboardMarkup из библиотеки telegram
    """
    return ReplyKeyboardMarkup([['Радиационный мониторинг'],
                                ['Пункты наблюдения'],
                                [KeyboardButton('Отправить мою геопозицию',
                                                request_location=True)]], resize_keyboard=True)


def encryption(TOKEN_FOR_DB, line):
    """
    Функция сисметричного шифрования строковых данных first_name, last_name и username пользователя для последующей
    передачи шифрованных данных в базу данных для долговременного хранения
    :param TOKEN_FOR_DB: сгенерированный ключ-пароль для шифрования
    :param line: строковый объект шифрования
    :return: строковый объект ограниченной длины(10 символов) - зашифрованный теств
    """
    while line is not None:
        cryptoline = TOKEN_FOR_DB.encrypt(line.encode('utf-8'))
        return cryptoline[:10].decode('utf-8')
