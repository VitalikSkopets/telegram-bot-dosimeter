import logging
import logging.config
import os

__all__ = ("get_logger",)


FOLDER_LOG = "logs"
LOG_FILENAME = "main.log"
ERROR_LOG_FILENAME = "main-errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": """
                    %(asctime)s - %(processName)-10s - %(name)-10s - %(levelname)
                    -8s - (%(filename)s).%(funcName)s(%(lineno)d)-5s - %(message)s
                """,
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
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": "../%s/%s" % (FOLDER_LOG, LOG_FILENAME),
            "maxBytes": 10485760,  # 10Mb
            "backupCount": 2,
            "encoding": "utf-8",
        },
        "time_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "../%s/%s" % (FOLDER_LOG, ERROR_LOG_FILENAME),
            "when": "d",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "default": {
            "handlers": [
                "console",
                "rotating_file",
                "time_rotating_file",
            ],
            "propagate": True,
        }
    },
}


def create_log_folder(folder: str = FOLDER_LOG) -> None:
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name: str = __name__) -> logging.Logger:
    create_log_folder()
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
