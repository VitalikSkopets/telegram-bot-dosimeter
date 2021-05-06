import config
import locale
import re
from datetime import datetime
from geopy import distance
from typing import Final, Optional, Any
from loguru import logger
from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
from config import LOCATION_OF_MONITORING_POINTS, ADMINISTRATIVE_DIVISION
from mongodb import DB
from utilities import (main_keyboard,
                       get_html,
                       scraper,
                       text_messages,
                       greeting,
                       )

locale.setlocale(category=locale.LC_ALL, locale="Russian")
today: Final = datetime.now().strftime("%a %d-%b-%Y %H:%M")


class Handlers:

    @staticmethod
    def start(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик команды /start. При выборе пользователем команды /start возвращает приветственное сообщение
        и кнопки меню вместо стандартной клавиатуры

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        logger.info('User selected /start command')
        DB.add_db_start(user)
        update.message.reply_text(f"Приятно познакомится, <b>{user['first_name']}</b>!"
                                  + text_messages['start'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

    @staticmethod
    def help(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик команды /help. При выборе пользователем команды /help возвращает текстовое сообщение и кнопки
        меню вместо стандартной клавиатуры

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        logger.info('User selected /help command')
        DB.add_db_help(user)
        update.message.reply_text(text_messages['help'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

    @staticmethod
    def messages(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик входящего тествового сообщенаия от пользователя. Если в текствовм сообщении пользователя есть
        строка из списка greeting, функция возвращает пользователю приветственное текстовое сообщение и кнопки меню
        вместо стандартной клавиатуры. Если в сообщении пользователя строки невходящие в спсиок greeting, функция
        возвращает пользователю текстовое сообщение с предложением выбрать команду /help

        :param update: словарь Update с пользовательской информацией Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        text = update.message.text
        if text.lower() in greeting:
            logger.info('User sent a welcome text message')
            DB.add_db_messages(user)
            update.message.reply_text(f"Привет, <b>{user['first_name']}</b>!"
                                      + text_messages['greet'], reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
        else:
            logger.info('User sent unknown text message')
            update.message.reply_text(text_messages['unknown'], parse_mode=ParseMode.HTML)

    @staticmethod
    def radioactive_monitoring(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия кнопки "Радиационный мониторинг". В теле функция производит вызов кастомной функцию
        get_html(), которая осуществляет get-запрос и скрайринг html-структуры https://rad.org.by/monitoring/radiation
        на основе регулярного выражения. Результаты скрайпинга в виде строкового объекта вместе с текущей датой
        подставляются в интерполированную строку - ответное сообщение пользователю. Также, в теле функции происходит
        повторный вызов кастомной функцию get_html(), которая в результате скрайпига https://rad.org.by/radiation.xml
        возвращает строковые значения радиации всех пунктов наблюдения, после чего приводит строковые значения уровня
        радиации к типу данных число с плавающей точкой float() и расчитывает среднее арефметическое значение уровня
        радиации всех пунктов наблюдения. Среднее арефметическое значение уровня радиации, также подставляются в
        интерполированную строку - ответное сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        try:
            text_lst = str(get_html(url=config.URL2).find_all('span'))
            pattern = r"(?:...*)(радиационная...*загрязнения)(?:<\/span>)"
            text = re.findall(pattern, text_lst)
            indications = get_html().find_all('rad')
            avg_indication = sum([float(indication.text) for indication in indications]) / len(indications)
            logger.info('User press button "Radioactive monitoring"')
            DB.add_db_radioactive_monitoring(user)
            update.message.reply_text(f'По состоянию на <i>{today}</i> {text[0]}.'
                                      f'\n\nПо стране <i>среднее</i> значение уровня МД '
                                      f'гамма-излучения в сети пунктов радиационного мониторинга Министерства природных'
                                      f' ресурсов и охраны окружающей среды Беларусь по состоянию на сегодняшний день '
                                      f'составляет <b>{avg_indication:.2f}</b> мкЗв/ч.', parse_mode=ParseMode.HTML
                                      )
        except ZeroDivisionError:
            logger.exception('ERROR division by zero. Not available on the resource https://rad.org.by/radiation.xml',
                             traceback=True
                             )
            update.message.reply_text(f"К сожалению, <b>{user['first_name']}</b>, " + text_messages['info'],
                                      parse_mode=ParseMode.HTML
                                      )
        except Exception:
            logger.exception('ERROR while performing the radioactive_monitoring() function', traceback=True)
            update.message.reply_text(f"К сожалению, <b>{user['first_name']}</b>, " + text_messages['info'],
                                      parse_mode=ParseMode.HTML
                                      )

    @staticmethod
    def monitoring_points(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Пункты наблюдения". Возвращает пользователю кнопк с названиями
        областей вместо стандартной клавиатуры

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        logger.info('User press button "Observation points"')
        DB.add_db_monitoring_points(user)
        update.message.reply_text(f'Выбери интересующий регион', reply_markup=ReplyKeyboardMarkup([
            ['Брестская область'], ['Витебская область'], ['Гомельская область'],
            ['Гродненская область'], ['Минск и Минская область'], ['Могилевская область'], ['Главное меню']],
            resize_keyboard=True)
                                  )

    @staticmethod
    def scraper_Brest(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Брестская область". Функция вызывет метод scraper(), которая,
        в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Брестской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Брестская область"])
        logger.info('User press button "Brest region"')
        DB.add_db_scraper_Brest(user)

    @staticmethod
    def scraper_Vitebsk(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Витебская область". Функция вызывет метод scraper(), которая,
        в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Витебской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Витебская область"])
        logger.info('User press button "Vitebsk region"')
        DB.add_db_scraper_Vitebsk(user)

    @staticmethod
    def scraper_Gomel(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Гомельская область". Функция вызывет метод scraper(), которая,
        в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Гомельской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Гомельская область"])
        logger.info('User press button "Gomel region"')
        DB.add_db_scraper_Gomel(user)

    @staticmethod
    def scraper_Grodno(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Гродненская область". Функция вызывет метод scraper(), которая,
        в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Гродненской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Гродненская область"])
        logger.info('User press button "Grodno region"')
        DB.add_db_scraper_Grodno(user)

    @staticmethod
    def scraper_Minsk(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Минск и Минская область". Функция вызывет метод scraper(),
        которая, в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Минске и Минской области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Минск и Минская область"])
        logger.info('User press button "Minsk region"')
        DB.add_db_scraper_Minsk(user)

    @staticmethod
    def scraper_Mogilev(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Могилевская область". Функция вызывет метод scraper(), которая,
        в свою очередь, вызывает метод get_html(). Последний отправляет get-запрос и скрайпит html-структуру
        https://rad.org.by/radiation.xml . Результаты скрайпинга в цикле for сравниваются на равенство с названиями
        пунктов наблюдения, расположенныъ в Могилевскойй области, и вместе с текущей датой подставляются в ответное
        сообщение пользователю

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        scraper(update, region=ADMINISTRATIVE_DIVISION["Могилевская область"])
        logger.info('User press button "Mogilev region"')
        DB.add_db_scraper_Mogilev(user)

    @staticmethod
    def master_menu(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия пользователем кнопки "Главное меню". В качестве ответного сообщения пользователю
        обработчик вызывает кастомную функцию main_keyboard(), которая возвращает пользователю сообщение и кнопки меню
        вместо стандартной клавиатуры

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        logger.info('User press button "Main menu"')
        update.message.reply_text(f'''<b>{user['first_name']}</b>, чтобы узнать по состоянию на <i>текущую дату</i> '''
                                  f'''уровень мощности эквивалентной дозы гамма-излучения, зафиксированного '''
                                  f'''на <i>ближайшем</i> пункте наблюдения, нажми <b>"Отправить мою геопозицию"</b>'''
                                  f'''\n\nЧтобы узнать обстановку в сети радиационного мониторинга Беларуси, нажми ''' 
                                  f'''<b>"Радиационный мониторинг"</b>\n\nЧтобы узнать сводку пунктов наблюдения в ''' 
                                  f'''сети радиационного мониторинга, нажми <b>"Пункты наблюдения"</b> и выбери ''' 
                                  f'''интересующий регион''', reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
                                  )

    @staticmethod
    def geolocation(update: Optional[Any], context: CallbackContext) -> None:
        """
        Функция-обработчик нажатия кнопки "Отправить мою геолокацию". В теле функции происходит вызов метода distance()
        из библиотеки geopy, которому в качестве оргументов передаются географические координаты пользователя и пунктов
        наблюдения из словаря LOCATION_OF_MONITORING_POINTS. Метод distance() расчитывает расстояние в метрах от каждого
        пункта наблюдения до пользователя. С помощью встроенной функции min() определяется расстояние до ближайшего
        к пользователю пунтка наблюдения. Также, в теле функция производит вызов кастомной функцию get_html(), которая
        осуществляет скрайпинг html-структуры https://rad.org.by/radiation.xml. Результаты выполнения метода distance()
        и функции скрайпинга вместе с текущей датой и временем подставляются в интерполированную строку, которая
        отправляется пользователю в качестве ответного сообщения

        :param update: словарь Update с информацией о пользователе Telegram

        :param context: class telegram.ext.CallbackContext(dispatcher)

        :return: None
        """
        user = update.effective_user
        try:
            user_location = update.message.location
            coordinates = (user_location.latitude, user_location.longitude)
            distance_list = []
            for point, location in LOCATION_OF_MONITORING_POINTS.items():
                distance_list.append((distance.distance(coordinates, location).km, point))
            min_distance = min(distance_list)
            points, indications = get_html().find_all('title'), get_html().find_all('rad')
            points.reverse()
            indications.reverse()
            zipped_values = zip(points, indications)
            zipped_list = list(zipped_values)
            for i in range(0, len(zipped_list)):
                if min_distance[1] == points[i].text:
                    logger.info('User press button "Send geolocation"')
                    DB.add_db_geolocation(user)
                    update.message.reply_text(f'<i>{min_distance[0]:.3f} м</i> до ближайшего пункта наблюдения '
                                              f'"{min_distance[1]}".\n\nВ пункте наблюдения "{points[i].text}" '
                                              f'по состоянию на <i>{today}</i> уровень эквивалентной дозы радиации '
                                              f'составляет <b>{indications[i].text}</b> мкЗв/ч.',
                                              parse_mode=ParseMode.HTML
                                              )
                    break
        except Exception:
            logger.exception('ERROR while performing the geolocation() function', traceback=True)
            update.message.reply_text(f"К сожалению, <b>{user['first_name']}</b>, " + text_messages['info'],
                                      parse_mode=ParseMode.HTML
                                      )
