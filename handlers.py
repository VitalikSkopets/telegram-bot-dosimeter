from bs4 import BeautifulSoup
from geopy import distance
import logging
import re
import requests
import datetime
from fake_useragent import UserAgent
from telegram import ParseMode
import config
from config import LOCATION_OF_MONITORING_POINTS
from utilities import main_keyboard, avg_rad, text_messages
from mongodb import (mdb, add_db_send_welcome,
                     add_db_send_help,
                     add_db_get_text_messages,
                     add_db_radioactive_monitoring,
                     add_db_scraper,
                     add_db_geolocation
                     )


def send_welcome(update, context):
    '''
    Функция-обработчик команды /start
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_send_welcome(mdb, message_inf)
    logging.info('User selected /start command and added in db')
    update.message.reply_text(f"Приятно познакомится, <b>{message_inf['message']['chat']['first_name']}</b>!"
                              + text_messages['start'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)


def send_help(update, context):
    '''
    Функция-обработчик команды /help
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_send_help(mdb, message_inf)
    logging.info('User selected /help command')
    update.message.reply_text(text_messages['help'], parse_mode=ParseMode.HTML)


def get_text_messages(update, context):
    '''
    Функция-обработчик входящего тествового сообщенаия от пользователя
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_get_text_messages(mdb, message_inf)
    text = update.message.text
    if text.lower() == 'привет' or text.lower() == 'hello':
        logging.info('User sent a welcome text message')
        update.message.reply_text(f"Привет, <b>{message_inf['message']['chat']['first_name']}</b>!"
                                  + text_messages['greet'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    else:
        logging.info('User sent unknown text message')
        update.message.reply_text(text_messages['unknown'], parse_mode=ParseMode.HTML)


def radioactive_monitoring(update, context):
    '''
    Функция-обработчик нажатия кнопки "Радиационный мониторинг"
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_radioactive_monitoring(mdb, message_inf)
    today = datetime.datetime.today().strftime("%a %d-%b-%Y")
    responce = requests.get(config.URL2, headers={'User-Agent': UserAgent().chrome})
    pattern = r"(?:\bsans-serif;\">)(По состоянию на)(?:...*)?(текущую дату)</span>&nbsp;(радиационная...*загрязнения)"
    text_tup = re.findall(pattern, responce.text)
    text_lst = list(zip(*text_tup))
    a, b, c = list(text_lst[0]), list(text_lst[1]), list(text_lst[2])
    abc = a + b + c
    abc[1] = today
    logging.info('User press button "Radioactive monitoring"')
    update.message.reply_text(f'{abc[0]} {abc[1]} {abc[2]}.\n\nПо стране <i>среднее</i> значение уровня МД '
                              f'гамма-излучения в сети пунктов радиационного мониторинга Министерства природных '
                              f'ресурсов и охраны окружающей среды Беларусь по состоянию на сегодняшний день '
                              f'составляет <b>{avg_rad()}</b>.', parse_mode=ParseMode.HTML)


def scraper(update, context):
    '''
    Функция-обработчик нажатия кнопки "Пункты наблюдения"
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_scraper(mdb, message_inf)
    response = requests.get(config.URL1, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'html.parser')
    points, today, indications = soup.find_all('title'), soup.find_all('pubdate'), soup.find_all('rad')
    points.reverse()
    today.reverse()
    indications.reverse()
    zipped_values = zip(points, today, indications)
    zipped_list = list(zipped_values)
    logging.info('User press button "Observation points"')
    update.message.reply_text(f'| *Пункт наблюдения* | *Дата и время* | *МД гамма-излучения* |',
                              parse_mode=ParseMode.MARKDOWN)
    for i in range(0, len(zipped_list)):
        update.message.reply_text(f'| "*{points[i].text}*" | _{today[i].text}_ | *{indications[i].text} мкЗв/ч* |',
                                  parse_mode=ParseMode.MARKDOWN)


def geolocation(update, context):
    '''
    Функция-обработчик нажатия кнопки "Отправить мою геолокацию"
    :param update: словарь с информацией о пользователе Telegram
    :param context:
    :return: None
    '''
    message_inf = update
    add_db_geolocation(mdb, message_inf)
    coordinates = update.message.location
    user_coordinates = (coordinates['latitude'], coordinates['longitude'])
    distance_list = []
    min_distance = float()
    for point, location in LOCATION_OF_MONITORING_POINTS.items():
        distance_list.append((distance.distance(user_coordinates, location).km, point))
        min_distance = min(distance_list)
    response = requests.get(config.URL1, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'html.parser')
    points, today, indications = soup.find_all('title'), soup.find_all('pubdate'), soup.find_all('rad')
    points.reverse()
    today.reverse()
    indications.reverse()
    zipped_values = zip(points, today, indications)
    zipped_list = list(zipped_values)
    for i in range(0, len(zipped_list)):
        if min_distance[1] == points[i].text:
            logging.info('User press button "Send geolocation"')
            update.message.reply_text(f'<i>{min_distance[0]:.3f} м</i> до ближайшего пункта наблюдения '
                                      f'"{min_distance[1]}".\n\nВ пункте наблюдения "{points[i].text}" по состоянию '
                                      f'на <i>{today[i].text}</i> уровень эквивалентной дозы радиации составляет '
                                      f'<b>{indications[i].text} мкЗв/ч</b>.', parse_mode=ParseMode.HTML)