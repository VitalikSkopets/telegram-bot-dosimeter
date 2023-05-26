import os
import pathlib
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import ParseResult, urlparse

import pytz
import sentry_sdk
from mtranslate import translate
from pydantic import BaseSettings, Field

__all__ = (
    "APP",
    "ASYMMETRIC_ENCRYPTION",
    "BASE_DIR",
    "DEBUG",
    "HEROKU_APP",
    "PORT",
    "PWD",
    "SENTRY_SDK",
    "TEMPLATES_DIR",
    "TESTS_DIR",
    "TOKEN",
    "TODAY",
    "UTF",
    "WEBHOOK_MODE",
    "AnalyticsSettings",
    "DataBaseSettings",
    "Key",
)

DEFAULT_LOCALE = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

DEBUG = True
ENVIRON = "DEV" if DEBUG else "PROD"
WEBHOOK_MODE = bool(0) if DEBUG else bool(1)

APP = "dosimeter"
BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
APP_DIR: pathlib.Path = BASE_DIR / APP
TEMPLATES_DIR: pathlib.Path = APP_DIR / "templates"
TESTS_DIR: pathlib.Path = BASE_DIR / "tests"
ENV_FILE = ".env"
UTF = "utf-8"

# python-telegram-bot API TOKEN
TOKEN = os.environ["API_TOKEN"]

MAIN_ADMIN_TELEGRAM_ID = int(os.environ["MAIN_ADMIN_TELEGRAM_ID"])
ADMIN_TELEGRAM_ID = int(os.environ["ADMIN_TELEGRAM_ID"])

# Heroku
HEROKU_APP = os.environ["HEROKU_APP"]
PORT = int(os.environ["PORT"])

# Sentry SDK
SENTRY_SDK = os.environ["SENTRY_SDK"]
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)

# Encryption
PWD = os.environ["PASS"]
ASYMMETRIC_ENCRYPTION = False


@dataclass(frozen=True)
class Key:
    SECRET: pathlib.Path = BASE_DIR / "secret.pem"
    PUBLIC: pathlib.Path = BASE_DIR / "public.pem"


# MongoDB Atlas
class DataBaseSettings(BaseSettings):
    host: str = Field(..., env="MONGO_HOST")
    username: str = Field(..., env="MONGO_USERNAME")
    password: str = Field(..., env="MONGO_PASSWORD")
    db_name: str = Field(..., env="MONGO_NAME")
    port: int = Field(default="8443")
    timeout: int = Field(default="5000")

    class Config:
        env_file = ENV_FILE
        env_prefix = "MONGO_"
        env_file_encoding = UTF

    @property
    def uri(self) -> str:
        return (
            f"mongodb+srv://{self.username}:{self.password}@cluster.s3cxd.mongodb.net/"
            f"{self.db_name}?retryWrites=true&w=majority"
        )


# Measurement Protocol API (Google Analytics 4)
class AnalyticsSettings(BaseSettings):
    measurement_id: str = Field(..., env="GOOGLE_MEASUREMENT_ID")
    api_secret: str = Field(..., env="GOOGLE_API_SECRET")

    class Config:
        env_file = ENV_FILE
        env_prefix = "GOOGLE_"
        env_file_encoding = UTF

    @property
    def url(self) -> ParseResult:
        return urlparse(
            f"https://www.google-analytics.com/mp/collect?"
            f"measurement_id={self.measurement_id}&api_secret={self.api_secret}"
        )
