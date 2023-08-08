import enum
from datetime import date, datetime
from typing import Sequence
from urllib.parse import ParseResult, urlparse

import pytest
from mtranslate import translate

from dosimeter.config import Settings


class Service(str, enum.Enum):
    """
    Service enumeration class for their configuration settings.
    """

    APP = "app"
    ENC = "enc"
    DB = "db"
    ANALYTICS = "analytics"
    HEROKU = "heroku"

    def __str__(self) -> str:
        return self.value


schema_settings = {
    Service.ANALYTICS: {
        "api_secret": None,
        "measurement_id": None,
    },
    Service.APP: {
        "admin_tgm_id": None,
        "debug": None,
        "locale": None,
        "main_admin_tgm_id": None,
        "name": None,
        "source": None,
        "timezone": None,
        "token": None,
    },
    Service.DB: {
        "host": None,
        "name": None,
        "password": None,
        "timeout": None,
        "username": None,
    },
    Service.ENC: {
        "isAsymmetric": None,
        "key": {
            "SECRET": None,
            "PUBLIC": None,
        },
        "pwd": None,
    },
    Service.HEROKU: {
        "app": None,
        "port": None,
    },
}


@pytest.mark.settings()
class TestSettings(object):
    """
    A class for testing settings configuration.
    """

    config = Settings()

    @pytest.mark.parametrize("service", Service)
    def test_settings_of_base_config(self, service: str) -> None:
        # Assert
        assert isinstance(self.config, Settings)
        assert service in self.config.dict().keys()

    @pytest.mark.parametrize(
        "service,keys",
        (
            [Service.APP, schema_settings.get(Service.APP).keys()],
            [Service.ENC, schema_settings.get(Service.ENC).keys()],
            [Service.DB, schema_settings.get(Service.DB).keys()],
            [Service.ANALYTICS, schema_settings.get(Service.ANALYTICS).keys()],
            [Service.HEROKU, schema_settings.get(Service.HEROKU).keys()],
        ),
        ids=list(Service),
    )
    def test_services_settings(self, service: str, keys: Sequence[str]) -> None:
        # Assert
        for key in keys:
            assert key in self.config.dict().get(service).keys()

    @pytest.mark.slow()
    @pytest.mark.freeze_time("2023-05-21")
    def test_freeze_date_today_for_settings(
        self,
    ) -> None:
        # Assert
        assert isinstance(self.config.app.today, str)
        assert self.config.app.today == "21 мая 2023 г."

    @pytest.mark.slow()
    def test_date_today_for_settings(self) -> None:
        # Act
        date_string = translate(self.config.app.today, "en")
        date_object = datetime.strptime(date_string, "%B %d, %Y")

        # Assert
        assert isinstance(date_object, datetime)
        assert date_object.date() == date.today()

    def test_heroku_webhook_uri_settings(self) -> None:
        # Act
        url = urlparse(self.config.heroku.webhook_uri)

        # Assert
        assert isinstance(self.config.heroku.webhook_uri, str)
        assert isinstance(url, ParseResult)
        assert self.config.heroku.app in url.hostname
