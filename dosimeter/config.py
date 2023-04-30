import logging
import logging.config
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, MutableMapping

import pytz
import sentry_sdk
from mtranslate import translate

__all__ = (
    "APP",
    "API_SECRET",
    "ASYMMETRIC_ENCRYPTION",
    "BASE_DIR",
    "DEBUG",
    "GOOGLE_DOMEN",
    "HEROKU_APP",
    "MONGO_DB_CONNECTION",
    "MONGO_DB_NAME",
    "PORT",
    "PWD",
    "PROTOKOL",
    "MEASUREMENT_ID",
    "SENTRY_SDK",
    "TEMPLATES_DIR",
    "TESTS_DIR",
    "TOKEN",
    "TODAY",
    "URL_RADIATION",
    "URL_MONITORING",
    "WEBHOOK_MODE",
    "CustomAdapter",
    "get_logger",
)

DEFAULT_LOCALE = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

DEBUG = True
ENVIRON = "DEV" if DEBUG else "PROD"
WEBHOOK_MODE = bool(0) if DEBUG else bool(1)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
TEMPLATES_DIR: Path = BASE_DIR / "templates"
TESTS_DIR: Path = BASE_DIR / "tests"

APP = "dosimeter"

# python-telegram-bot API TOKEN
TOKEN = os.environ["API_TOKEN"]

MAIN_ADMIN_TELEGRAM_ID = int(os.environ["MAIN_ADMIN_TELEGRAM_ID"])
ADMIN_TELEGRAM_ID = int(os.environ["ADMIN_TELEGRAM_ID"])

# MongoDB Atlas
MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]
MONGO_DB_LOGIN = os.environ["MONGO_DB_LOGIN"]
MONGO_DB_PASSWORD = os.environ["MONGO_DB_PASSWORD"]
MONGO_DB_HOST = os.environ["MONGO_DB_HOST"]
MONGO_DB_CONNECTION = (
    f"mongodb+srv://{MONGO_DB_LOGIN}:{MONGO_DB_PASSWORD}@cluster.s3cxd.mongodb.net/"
    f"{MONGO_DB_NAME}?retryWrites=true&w=majority"
)

# Encryption
PWD = os.environ["PASS"]
ASYMMETRIC_ENCRYPTION = False

# Heroku
HEROKU_APP = os.environ["HEROKU_APP"]
PORT = int(os.environ["PORT"])

# Source data
URL_RADIATION = f"{os.environ['DEFAULT_URL']}/radiation.xml"
URL_MONITORING = f"{os.environ['DEFAULT_URL']}/monitoring/radiation"

# Measurement Protocol API (Google Analytics 4)
GOOGLE_DOMEN = "www.google-analytics.com"
PROTOKOL = "https"
MEASUREMENT_ID = os.environ["MEASUREMENT_ID"]

# Google Analytics
API_SECRET = os.environ["API_SECRET"]

# Logging
FOLDER_LOG = "logs"
LOG_FILENAME = "main.log"
ERROR_LOG_FILENAME = "errors.log"


class EnvironFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.environment = ENVIRON  # type: ignore
        return True


class RequestFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = str(uuid.uuid4())  # type: ignore
        return True


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "environ_filter": {
            "()": EnvironFilter,
        },
        "request_filter": {
            "()": RequestFilter,
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(environment)s] - %(processName)-10s"
            " - %(name)-10s - %(levelname)-8s - (%(filename)s).%(funcName)s(%(lineno)d)"
            " - request_id: [%(request_id)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "brief": {
            "format": "%(asctime)s - [%(environment)s] - %(levelname)-8s -"
            " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                    asctime: %(asctime)s
                    environment: %(environment)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    request_id: %(request_id)s
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
            "formatter": "brief",
            "filters": ["environ_filter"],
            "stream": "ext://sys.stdout",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["environ_filter", "request_filter"],
            "filename": f"{BASE_DIR}/{FOLDER_LOG}/{LOG_FILENAME}",
            "maxBytes": 10485760,  # 10Mb
            "backupCount": 2,
            "encoding": "utf-8",
        },
        "time_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filters": ["environ_filter", "request_filter"],
            "filename": f"{BASE_DIR}/{FOLDER_LOG}/{ERROR_LOG_FILENAME}",
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


def create_log_folder(folder_name: str = FOLDER_LOG) -> None:
    folder = Path(BASE_DIR / folder_name)
    folder.mkdir(exist_ok=True)


def get_logger(name: str = __name__, template: str = "file_logger") -> logging.Logger:
    create_log_folder()
    template = "console_logger" if DEBUG else template
    LOGGING_CONFIG["loggers"][name] = LOGGING_CONFIG["loggers"][template]
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: Any) -> tuple[str, MutableMapping[str, Any]]:
        context = kwargs.pop("user_id", self.extra["user_id"])  # type: ignore[index]
        return "user_id: [%s] - %s" % (context, msg), kwargs


# Sentry SDK
SENTRY_SDK = os.environ["SENTRY_SDK"]
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)
