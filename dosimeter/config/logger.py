import enum
import logging
import logging.config
import uuid
from pathlib import Path
from typing import Any, MutableMapping

from dosimeter.config import config, settings

__all__ = ("CustomAdapter", "get_logger")


class LOGRoutes(str, enum.Enum):
    FOLDER = "logs"
    FILE = "main.log"
    ERR_FILE = "errors.log"

    def __str__(self) -> str:
        return self.value


class EnvironFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "environment", config.app.environ)
        return True


class RequestFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "request_id", str(uuid.uuid4()))
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
            "filename": f"{settings.BASE_DIR}/{LOGRoutes.FOLDER}/{LOGRoutes.FILE}",
            "maxBytes": 10485760,  # 10Mb
            "backupCount": 2,
            "encoding": "utf-8",
        },
        "time_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filters": ["environ_filter", "request_filter"],
            "filename": f"{settings.BASE_DIR}/{LOGRoutes.FOLDER}/{LOGRoutes.ERR_FILE}",
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


def create_log_folder(folder_name: str = LOGRoutes.FOLDER) -> None:
    folder = Path(settings.BASE_DIR / folder_name)
    folder.mkdir(exist_ok=True)


def get_logger(name: str = __name__, template: str = "file_logger") -> logging.Logger:
    create_log_folder()
    template = "console_logger" if config.app.debug else template
    LOGGING_CONFIG["loggers"][name] = LOGGING_CONFIG["loggers"][template]
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: Any) -> tuple[str, MutableMapping[str, Any]]:
        context = kwargs.pop("user_id", self.extra["user_id"])  # type: ignore[index]
        return "user_id: [%s] - %s" % (context, msg), kwargs
