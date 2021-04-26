import re
from datetime import datetime
import locale
from geopy import distance
from loguru import logger
from telegram import ReplyKeyboardMarkup, ParseMode
import config
from config import LOCATION_OF_MONITORING_POINTS, ADMINISTRATIVE_DIVISION
from mongodb import (mdb, add_db_start,
                     add_db_help,
                     add_db_messages,
                     add_db_radioactive_monitoring,
                     add_db_monitoring_points,
                     add_db_scraper_Brest,
                     add_db_scraper_Vitebsk,
                     add_db_scraper_Gomel,
                     add_db_scraper_Grodno,
                     add_db_scraper_Minsk,
                     add_db_scraper_Mogilev,
                     add_db_geolocation
                     )
from utilities import (main_keyboard,
                       avg_rad,
                       get_html,
                       scraper,
                       text_messages,
                       greeting
                       )

locale.setlocale(category=locale.LC_ALL, locale="Russian")
today = datetime.now().strftime("%a %d-%b-%Y %H:%M")


def start(update, context):
    """
    Функция-обработчик команды /start
    :param update: словарь Update с информацией о пользователе Telegram
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
    :param update: словарь Update с информацией о пользователе Telegram
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
    :param update: словарь Update с пользовательской информацией Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    text = update.message.text
    if text.lower() in greeting:
        logger.info('User sent a welcome text message')
        add_db_messages(mdb, user)
        update.message.reply_text(f"Привет, <b>{user['first_name']}</b>!"
                                  + text_messages['greet'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    else:
        logger.info('User sent unknown text message')
        update.message.reply_text(text_messages['unknown'], parse_mode=ParseMode.HTML)


def radioactive_monitoring(update, context):
    """
    Функция-обработчик нажатия кнопки "Радиационный мониторинг". В теле функция производит get-запрос на
    https://rad.org.by/monitoring/radiation и скрайринг html-структуры на основе регулярного выражения.
    Результаты скрайпинга вместе с текущей датой подставляются в ответное сообщение, которое бот отправляет
    пользователю вместе с результатом вызова кастомной функции avg_rad()
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    text_lst = str(get_html(url=config.URL2).find_all('span'))
    pattern = r"(?:...*)(радиационная...*загрязнения)(?:<\/span>)"
    text = re.findall(pattern, text_lst)
    logger.info('User press button "Radioactive monitoring"')
    add_db_radioactive_monitoring(mdb, user)
    update.message.reply_text(f'По состоянию на <i>{today}</i> {text[0]}.'
                              f'\n\nПо стране <i>среднее</i> значение уровня МД '
                              f'гамма-излучения в сети пунктов радиационного мониторинга Министерства природных '
                              f'ресурсов и охраны окружающей среды Беларусь по состоянию на сегодняшний день '
                              f'составляет <b>{avg_rad()}</b>.', parse_mode=ParseMode.HTML)


def monitoring_points(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Пункты наблюдения". Возвращает пользователю кнопк с названиями
    областей вместо стандартной клавиатуры
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    logger.info('User press button "Observation points"')
    add_db_monitoring_points(mdb, user)
    update.message.reply_text(f'Выбери интересующий регион', reply_markup=ReplyKeyboardMarkup([
        ['Брестская область'], ['Витебская область'], ['Гомельская область'],
        ['Гродненская область'], ['Минск и Минская область'], ['Могилевская область']], resize_keyboard=True)
                              )


def scraper_Brest(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Брестская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Брестской области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Брестская область"])
    logger.info('User press button "Brest region"')
    add_db_scraper_Brest(mdb, user)


def scraper_Vitebsk(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Витебская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Витебской области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Витебская область"])
    logger.info('User press button "Vitebsk region"')
    add_db_scraper_Vitebsk(mdb, user)


def scraper_Gomel(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Гомельская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Гомельской области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Гомельская область"])
    logger.info('User press button "Gomel region"')
    add_db_scraper_Gomel(mdb, user)


def scraper_Grodno(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Гродненская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Гродненской области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Гродненская область"])
    logger.info('User press button "Grodno region"')
    add_db_scraper_Grodno(mdb, user)


def scraper_Minsk(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Минск и Минская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Минске и Минской области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Минск и Минская область"])
    logger.info('User press button "Minsk region"')
    add_db_scraper_Minsk(mdb, user)


def scraper_Mogilev(update, context):
    """
    Функция-обработчик нажатия пользователем кнопки "Могилевская область". Функция вызывет метод scraper(), которая,
    в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
    https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
    пунктов наблюдения, расположенныъ в Могилевскойй области, и вместе с текущей датой подставляются в ответное
    сообщение пользователю
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    scraper(update, region=ADMINISTRATIVE_DIVISION["Могилевская область"])
    logger.info('User press button "Mogilev region"')
    add_db_scraper_Mogilev(mdb, user)


def geolocation(update, context):
    """
    Функция-обработчик нажатия кнопки "Отправить мою геолокацию"
    :param update: словарь Update с информацией о пользователе Telegram
    :param context: CallbackContext
    :return: None
    """
    user = update.effective_user
    user_location = update.message.location
    coordinates = (user_location.latitude, user_location.longitude)
    distance_list = []
    for point, location in LOCATION_OF_MONITORING_POINTS.items():
        distance_list.append((distance.distance(coordinates, location).km, point))
    min_distance = min(distance_list)
    points = get_html().find_all('title')
    indications = get_html().find_all('rad')
    points.reverse()
    indications.reverse()
    zipped_values = zip(points, indications)
    zipped_list = list(zipped_values)
    for i in range(0, len(zipped_list)):
        if min_distance[1] == points[i].text:
            logger.info('User press button "Send geolocation"')
            add_db_geolocation(mdb, user)
            update.message.reply_text(f'<i>{min_distance[0]:.3f} м</i> до ближайшего пункта наблюдения '
                                      f'"{min_distance[1]}".\n\nВ пункте наблюдения "{points[i].text}" по состоянию '
                                      f'на <i>{today}</i> уровень эквивалентной дозы радиации составляет '
                                      f'<b>{indications[i].text} мкЗв/ч</b>.', parse_mode=ParseMode.HTML)
            break
