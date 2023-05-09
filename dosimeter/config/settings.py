import os
from datetime import datetime
from pathlib import Path

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
    "WEBHOOK_MODE",
)

DEFAULT_LOCALE = "ru"
DATE: str = datetime.now(pytz.timezone("Europe/Minsk")).strftime("%d-%b-%Y")
TODAY: str = translate(DATE, DEFAULT_LOCALE)

DEBUG = True
ENVIRON = "DEV" if DEBUG else "PROD"
WEBHOOK_MODE = bool(0) if DEBUG else bool(1)

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
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

# Measurement Protocol API (Google Analytics 4)
GOOGLE_DOMEN = "www.google-analytics.com"
PROTOKOL = "https"
MEASUREMENT_ID = os.environ["MEASUREMENT_ID"]

# Google Analytics
API_SECRET = os.environ["API_SECRET"]

# Sentry SDK
SENTRY_SDK = os.environ["SENTRY_SDK"]
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)
