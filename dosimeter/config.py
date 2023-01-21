import logging
import logging.config
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import pytz
import sentry_sdk
from mtranslate import translate

__all__ = (
    "API_SECRET",
    "ASYMMETRIC_ENCRYPTION",
    "BASE_DIR",
    "DEBUG",
    "GOOGLE_DOMEN",
    "MONGO_DB_NAME",
    "PORT",
    "HEROKU_APP",
    "PWD",
    "WEBHOOK_MODE",
    "PROTOKOL",
    "MEASUREMENT_ID",
    "SENTRY_SDK",
    "TOKEN",
    "TODAY",
    "URL_RADIATION",
    "URL_MONITORING",
    "get_logger",
    "CustomAdapter",
)

DEFAULT_LOCALE: str = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

DEBUG: bool = True
ENVIRON: str = "DEV" if DEBUG else "PROD"

BASE_DIR = Path(__file__).resolve().parent.parent

# python-telegram-bot API TOKEN
TOKEN: str = os.getenv("API_TOKEN", "1701801984:AAHb4Gl75jSqiC-uIVGuDRdK54ueEIfNQps")

# MongoDB Atlas
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "users_db")
MONGO_DB_LOGIN: str = os.getenv("MONGO_DB_LOGIN", "DosimeterBot")
MONGO_DB_PASSWORD: str = os.getenv("MONGO_DB_PASSWORD", "dG7ntC7sa1RrDpBp")
MONGO_DB_HOST: str = os.getenv("MONGO_DB_HOST", "cluster")

# Encryption
PWD: str = os.getenv(
    "PASS", "N1dzNXJKMWZSWXBWZWpDSVk4NVFZSkR2dHhxWWpnUjg5Rk9HaTVFSDF5Yz0="
)
ASYMMETRIC_ENCRYPTION: bool = False

# Heroku
HEROKU_APP: str = os.getenv("HEROKU_APP", "")
WEBHOOK_MODE: bool = bool(os.getenv("WEBHOOK_MODE", 0))
PORT: int = int(os.getenv("PORT", "8443"))

# Source data
URL_RADIATION: str = os.getenv("URL_RADIATION", "https://rad.org.by/radiation.xml")
URL_MONITORING: str = os.getenv(
    "URL_MONITORING", "https://rad.org.by/monitoring/radiation"
)

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
    def process(self, msg, kwargs):  # type: ignore
        context = kwargs.pop("user_id", self.extra["user_id"])
        return "user_id: [%s] - %s" % (context, msg), kwargs


# Sentry SDK
SENTRY_SDK: str = os.getenv("SENTRY_SDK", "")
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)
