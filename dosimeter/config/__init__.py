import os
import pathlib
from datetime import datetime
from urllib.parse import ParseResult, urlparse

import pytz
import sentry_sdk
from mtranslate import translate
from pydantic import BaseModel, BaseSettings, Field

BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
ENV_FILE = ".env"
UTF = "utf-8"


# Heroku
class HerokuCloudSettings(BaseSettings):
    app: str = Field(..., env="HEROKU_APP")
    port: int = Field(..., env="HEROKU_PORT")

    class Config:
        env_file = ENV_FILE
        env_prefix = "HEROKU_"
        env_file_encoding = UTF

    @property
    def webhook_uri(self) -> str:
        return urlparse(f"https://{self.app}.herokuapp.com").geturl()


# Encryption
class Key(BaseModel):
    SECRET: pathlib.Path = BASE_DIR / "secret.pem"
    PUBLIC: pathlib.Path = BASE_DIR / "public.pem"


class EncryptionSettings(BaseSettings):
    pwd: str = Field(..., env="ENC_PWD")
    isAsymmetric: bool = Field(default=False)
    key: Key = Key()

    class Config:
        env_file = ENV_FILE
        env_prefix = "ENC_"
        env_file_encoding = UTF


# Cloud Mongo Atlas Database
class CloudDataBaseSettings(BaseSettings):
    host: str = Field(..., env="MONGO_HOST")
    username: str = Field(..., env="MONGO_USERNAME")
    password: str = Field(..., env="MONGO_PASSWORD")
    name: str = Field(..., env="MONGO_NAME")
    timeout: int = Field(default=5_000)

    class Config:
        env_file = ENV_FILE
        env_prefix = "MONGO_"
        env_file_encoding = UTF

    @property
    def uri(self) -> str:
        return (
            f"mongodb+srv://{self.username}:{self.password}@cluster.s3cxd.mongodb.net/"
            f"{self.name}?retryWrites=true&w=majority"
        )


# File Database (Repository)
class FileDataBaseSettings(BaseSettings):
    stem: str = Field(default="dataBase")
    suffix: str = Field(default=".json")
    encoding: str = Field(default=UTF)

    @property
    def name(self) -> str:
        return self.stem + self.suffix

    @property
    def path(self) -> pathlib.Path:
        return BASE_DIR / "dosimeter" / "storage" / self.name


# Measurement Protocol API (Google Analytics 4)
class AnalyticsSettings(BaseSettings):
    measurement_id: str = Field(..., env="GOOGLE_MEASUREMENT_ID")
    api_secret: str = Field(..., env="GOOGLE_API_SECRET")

    class Config:
        env_file = ENV_FILE
        env_prefix = "GOOGLE_"
        env_file_encoding = UTF

    @property
    def uri(self) -> ParseResult:
        return urlparse(
            f"https://www.google-analytics.com/mp/collect?"
            f"measurement_id={self.measurement_id}&api_secret={self.api_secret}"
        )


# python-telegram-bot
class AppSettings(BaseSettings):
    token: str = Field(..., env="API_TOKEN")
    name: str = Field(default="dosimeter")
    source: str = Field(..., env="SOURCE")
    main_admin_tgm_id: int = Field(..., env="MAIN_ADMIN_TGM_ID")
    admin_tgm_id: int = Field(..., env="ADMIN_TGM_ID")
    locale: str = Field(default="ru")
    timezone: str = Field(default="Europe/Minsk")
    debug: bool = Field(default=True)

    class Config:
        env_file = ENV_FILE
        env_file_encoding = UTF

    @property
    def dir(self) -> pathlib.Path:
        return BASE_DIR / self.name

    @property
    def templates_dir(self) -> pathlib.Path:
        return self.dir / "templates"

    @property
    def chart_dir(self) -> pathlib.Path:
        return self.dir / "chart_engine" / "charts"

    @property
    def tests_dir(self) -> pathlib.Path:
        return BASE_DIR / "tests"

    @property
    def today(self) -> str:
        date = datetime.now(pytz.timezone(self.timezone)).strftime("%d-%b-%Y")
        return translate(date, self.locale)

    @property
    def date_format(self) -> str:
        return "%Y-%m-%d %H:%M:%S"

    @property
    def environ(self) -> str:
        return "DEV" if self.debug else "PROD"

    @property
    def webhook_mode(self) -> bool:
        return False if self.debug else True


class Settings(BaseModel):
    app: AppSettings = Field(default_factory=AppSettings)
    enc: EncryptionSettings = Field(default_factory=EncryptionSettings)
    db: CloudDataBaseSettings = Field(default_factory=CloudDataBaseSettings)
    repo: FileDataBaseSettings = Field(default_factory=FileDataBaseSettings)
    analytics: AnalyticsSettings = Field(default_factory=AnalyticsSettings)
    heroku: HerokuCloudSettings = Field(default_factory=HerokuCloudSettings)


"""Settings class instance"""
config = Settings()


# Sentry SDK
SENTRY_SDK = os.environ["SENTRY_SDK"]
sentry_sdk.init(dsn=SENTRY_SDK, traces_sample_rate=1.0)
