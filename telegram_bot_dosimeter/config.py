import locale
import os
from datetime import datetime

import pytz  # type: ignore
from mtranslate import translate

__all__ = (
    "TODAY",
    "TOKEN",
    "MONGO_DB_NAME",
    "MONGO_DB_LINK",
    "PORT",
    "HEROKU_APP_NAME",
    "WEBHOOK_MODE",
    "MEASUREMENT_ID",
    "API_SECRET",
    "URL_RADIATION",
    "URL_MONITORING",
)

locale.setlocale(category=locale.LC_ALL, locale="Russian")

DEFAULT_LOCALE: str = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

# python-telegram-bot API TOKEN
TOKEN: str = os.getenv("API_TOKEN", "")

# MongoDB Atlas
MONGO_DB_NAME: str | None = os.getenv("MONGO_DB_NAME")
MONGO_DB_LOGIN: str | None = os.getenv("MONGO_DB_LOGIN")
MONGO_DB_PASSWORD: str | None = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_LINK: str = f"""
    mongodb+srv://{MONGO_DB_LOGIN}:{MONGO_DB_PASSWORD}@cluster.s3cxd.mongodb.net/
    {MONGO_DB_NAME}?retryWrites=true&w=majority"""
PORT: int = int(os.getenv("PORT", "8443"))

# Heroku
HEROKU_APP_NAME: str | None = os.getenv("HEROKU_APP_NAME")
WEBHOOK_MODE: bool = bool(os.getenv("WEBHOOK_MODE", 1))

# Source data
URL_RADIATION: str | None = os.getenv("URL_RADIATION")
URL_MONITORING: str | None = os.getenv("URL_MONITORING")

# Measurement Protocol API (Google Analytics 4)
MEASUREMENT_ID: str | None = os.getenv("MEASUREMENT_ID")

# Google Analytics
API_SECRET: str | None = os.getenv("API_SECRET")

DESCRIPTION: str = """
    Этот бот может информировать пользователя по состоянию на текущую дату о
    радиационной обстановке в Беларуси и об уровне мощности эквивалентной дозы
    гамма-излучения, зафиксированного в сети радиационного мониторинга Министерства
    природных ресурсов и охраны окружающей среды Беларуси Источник: ©rad.org.by
    Разработано: ©itrexgroup.com
    """