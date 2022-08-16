import logging
import logging.config
from pathlib import Path

import sentry_sdk

__all__ = ("get_logger",)

from telegram_bot_dosimeter import config

FOLDER_LOG = "logs"
LOG_FILENAME = "main.log"
ERROR_LOG_FILENAME = "errors.log"

LOGGING_CONFIG = {
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
    if not folder.exists():
        folder.mkdir(exist_ok=True)


def get_logger(name: str = __name__, template: str = "file_logger") -> logging.Logger:
    create_log_folder()
    LOGGING_CONFIG["loggers"][name] = LOGGING_CONFIG["loggers"][template]  # type: ignore
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


def get_default_logger() -> logging.Logger:
    create_log_folder()
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger("console_logger")


# Sentry
sentry_sdk.init(dsn=config.SENTRY_SDK, traces_sample_rate=1.0)
