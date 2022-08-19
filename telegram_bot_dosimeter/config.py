import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pytz
import sentry_sdk
from mtranslate import translate

__all__ = (
    "TODAY",
    "DEBUG",
    "TOKEN",
    "MONGO_DB_NAME",
    "PORT",
    "HEROKU_APP_NAME",
    "WEBHOOK_MODE",
    "GOOGLE_DOMEN",
    "PROTOKOL",
    "MEASUREMENT_ID",
    "API_SECRET",
    "SENTRY_SDK",
    "URL_RADIATION",
    "URL_MONITORING",
    "get_logger",
)

DEFAULT_LOCALE: str = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

DEBUG: bool = False

# python-telegram-bot API TOKEN
TOKEN: str = os.getenv("API_TOKEN", "")

# MongoDB Atlas
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "")
MONGO_DB_LOGIN: str = os.getenv("MONGO_DB_LOGIN", "")
MONGO_DB_PASSWORD: str = os.getenv("MONGO_DB_PASSWORD", "")
MONGO_DB_HOST: str = os.getenv("MONGO_DB_HOST", "cluster")

# Heroku
HEROKU_APP_NAME: str = os.getenv("HEROKU_APP_NAME", "")
WEBHOOK_MODE: bool = bool(os.getenv("WEBHOOK_MODE", 1))
PORT: int = int(os.getenv("PORT", "8443"))

# Source data
URL_RADIATION: str = os.getenv("URL_RADIATION", "")
URL_MONITORING: str = os.getenv("URL_MONITORING", "")

# Measurement Protocol API (Google Analytics 4)
GOOGLE_DOMEN: str = "www.google-analytics.com"
PROTOKOL: str = "https"
MEASUREMENT_ID: str = os.getenv("MEASUREMENT_ID", "")

# Google Analytics
API_SECRET: str = os.getenv("API_SECRET", "")

# Logging
FOLDER_LOG: str = "logs"
LOG_FILENAME: str = "main.log"
ERROR_LOG_FILENAME: str = "errors.log"

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(processName)-10s - %(name)-10s - %(levelname)-8s"
            " - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": "%s/%s" % (FOLDER_LOG, LOG_FILENAME),
            "maxBytes": 10485760,  # 10Mb
            "backupCount": 2,
            "encoding": "utf-8",
        },
        "time_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "%s/%s" % (FOLDER_LOG, ERROR_LOG_FILENAME),
            "when": "d",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "file_logger": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "rotating_file",
                "time_rotating_file",
            ],
            "propagate": True,
        },
        "console_logger": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": True,
        },
    },
}


def create_log_folder(name: str = FOLDER_LOG) -> None:
    folder = Path(name)
    folder.mkdir(exist_ok=True)


def get_logger(name: str = __name__, template: str = "file_logger") -> logging.Logger:
    create_log_folder()
    template = "console_logger" if not DEBUG else template
    LOGGING_CONFIG["loggers"][name] = LOGGING_CONFIG["loggers"][template]
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


# Sentry SDK
SENTRY_SDK: str = os.getenv("SENTRY_SDK", "")
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)

DESCRIPTION: str = """
    Этот бот может информировать пользователя по состоянию на текущую дату о
    радиационной обстановке в Беларуси и об уровне мощности эквивалентной дозы
    гамма-излучения, зафиксированного в сети радиационного мониторинга Министерства
    природных ресурсов и охраны окружающей среды Беларуси Источник: ©rad.org.by
    Разработано: ©itrexgroup.com
    """
