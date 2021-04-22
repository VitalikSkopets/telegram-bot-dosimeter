from geopy import distance
from loguru import logger
import re
import requests
from datetime import datetime
from fake_useragent import UserAgent
from telegram import ParseMode
import config
from config import LOCATION_OF_MONITORING_POINTS
from utilities import (main_keyboard,
                       avg_rad,
                       get_html,
                       text_messages
                       )
from mongodb import (mdb, add_db_start,
                     add_db_help,
                     add_db_messages,
                     add_db_radioactive_monitoring,
                     add_db_scraper,
                     add_db_geolocation
                     )


def start(update, context):
    """
    Функция-обработчик команды /start
    :param update: Update словарь с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    logger.info('User selected /start command')
    add_db_start(mdb, user)
    update.message.reply_text(f"Приятно познакомится, <b>{user['first_name']}</b>!"
                              + text_messages['start'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)


def help(update, context):
    """
    Функция-обработчик команды /help
    :param update: Update словарь с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    logger.info('User selected /help command')
    add_db_help(mdb, user)
    update.message.reply_text(text_messages['help'], parse_mode=ParseMode.HTML)


def messages(update, context):
    """
    Функция-обработчик входящего тествового сообщенаия от пользователя
    :param update: Update словарь с пользовательской информацией Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    text = update.message.text
    if text.lower() == 'привет' or text.lower() == 'hello' or text.lower() == 'hi':
        logger.info('User sent a welcome text message')
        add_db_messages(mdb, user)
        update.message.reply_text(f"Привет, <b>{user['first_name']}</b>!"
                                  + text_messages['greet'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    else:
        logger.info('User sent unknown text message')
        update.message.reply_text(text_messages['unknown'], parse_mode=ParseMode.HTML)


def radioactive_monitoring(update, context):
    """
    Функция-обработчик нажатия кнопки "Радиационный мониторинг"
    :param update: Update словарь с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    today = datetime.now().strftime("%a %d-%b-%Y")
    responce = requests.get(config.URL2, headers={'User-Agent': UserAgent().chrome})
    pattern = r"(?:\bsans-serif;\">)(По состоянию на)(?:...*)?(текущую дату)</span>&nbsp;(радиационная...*загрязнения)"
    text_tup = re.findall(pattern, responce.text)
    text_lst = list(zip(*text_tup))
    a, b, c = list(text_lst[0]), list(text_lst[1]), list(text_lst[2])
    abc = a + b + c
    abc[1] = today
    logger.info('User press button "Radioactive monitoring"')
    add_db_radioactive_monitoring(mdb, user)
    update.message.reply_text(f'{abc[0]} {abc[1]} {abc[2]}.\n\nПо стране <i>среднее</i> значение уровня МД '
                              f'гамма-излучения в сети пунктов радиационного мониторинга Министерства природных '
                              f'ресурсов и охраны окружающей среды Беларусь по состоянию на сегодняшний день '
                              f'составляет <b>{avg_rad()}</b>.', parse_mode=ParseMode.HTML)


def scraper(update, context):
    """
    Функция-обработчик нажатия кнопки "Пункты наблюдения"
    :param update: Update словарь с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    points = get_html().find_all('title')
    today = get_html().find_all('pubdate')
    indications = get_html().find_all('rad')
    points.reverse()
    today.reverse()
    indications.reverse()
    zipped_values = zip(points, today, indications)
    zipped_list = list(zipped_values)
    logger.info('User press button "Observation points"')
    add_db_scraper(mdb, user)
    update.message.reply_text(f'| *Пункт наблюдения* | *Дата и время* | *МД гамма-излучения* |',
                              parse_mode=ParseMode.MARKDOWN)
    for i in range(0, len(zipped_list)):
        update.message.reply_text(f'| "*{points[i].text}*" | _{today[i].text}_ | *{indications[i].text} мкЗв/ч* |',
                                  parse_mode=ParseMode.MARKDOWN)


def geolocation(update, context):
    """
    Функция-обработчик нажатия кнопки "Отправить мою геолокацию"
    :param update: Update словарь с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    user_location = update.message.location
    coordinates = (user_location.latitude, user_location.longitude)
    distance_list = []
    min_distance = float()
    for point, location in LOCATION_OF_MONITORING_POINTS.items():
        distance_list.append((distance.distance(coordinates, location).km, point))
        min_distance = min(distance_list)
    points = get_html().find_all('title')
    today = get_html().find_all('pubdate')
    indications = get_html().find_all('rad')
    points.reverse()
    today.reverse()
    indications.reverse()
    zipped_values = zip(points, today, indications)
    zipped_list = list(zipped_values)
    for i in range(0, len(zipped_list)):
        if min_distance[1] == points[i].text:
            logger.info('User press button "Send geolocation"')
            add_db_geolocation(mdb, user)
            update.message.reply_text(f'<i>{min_distance[0]:.3f} м</i> до ближайшего пункта наблюдения '
                                      f'"{min_distance[1]}".\n\nВ пункте наблюдения "{points[i].text}" по состоянию '
                                      f'на <i>{today[i].text}</i> уровень эквивалентной дозы радиации составляет '
                                      f'<b>{indications[i].text} мкЗв/ч</b>.', parse_mode=ParseMode.HTML)
