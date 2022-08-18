import os
from datetime import datetime

import pytz
from mtranslate import translate

__all__ = (
    "TODAY",
    "TOKEN",
    "MONGO_DB_NAME",
    "PORT",
    "HEROKU_APP_NAME",
    "WEBHOOK_MODE",
    "MEASUREMENT_ID",
    "API_SECRET",
    "SENTRY_SDK",
    "URL_RADIATION",
    "URL_MONITORING",
)

DEFAULT_LOCALE: str = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

# python-telegram-bot API TOKEN
TOKEN: str = os.getenv("API_TOKEN", "")

# MongoDB Atlas
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "")
MONGO_DB_LOGIN: str = os.getenv("MONGO_DB_LOGIN", "")
MONGO_DB_PASSWORD: str = os.getenv("MONGO_DB_PASSWORD", "")
PORT: int = int(os.getenv("PORT", "8443"))

# Heroku
HEROKU_APP_NAME: str = os.getenv("HEROKU_APP_NAME", "")
WEBHOOK_MODE: bool = bool(os.getenv("WEBHOOK_MODE", 1))

# Source data
URL_RADIATION: str = os.getenv("URL_RADIATION", "")
URL_MONITORING: str = os.getenv("URL_MONITORING", "")

# Measurement Protocol API (Google Analytics 4)
MEASUREMENT_ID: str = os.getenv("MEASUREMENT_ID", "")

# Google Analytics
API_SECRET: str = os.getenv("API_SECRET", "")

# Sentry SDK
SENTRY_SDK: str = os.getenv("SENTRY_SDK", "")

DESCRIPTION: str = """
    Этот бот может информировать пользователя по состоянию на текущую дату о
    радиационной обстановке в Беларуси и об уровне мощности эквивалентной дозы
    гамма-излучения, зафиксированного в сети радиационного мониторинга Министерства
    природных ресурсов и охраны окружающей среды Беларуси Источник: ©rad.org.by
    Разработано: ©itrexgroup.com
    """
