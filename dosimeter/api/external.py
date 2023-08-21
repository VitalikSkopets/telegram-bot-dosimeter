from http import HTTPStatus
from urllib.parse import urlparse

import requests
import urllib3
from fake_useragent import UserAgent

from dosimeter.api.interface import BaseApi
from dosimeter.config.logger import get_logger
from dosimeter.constants import URL
from dosimeter.utils import timed_lru_cache

urllib3.disable_warnings()

logger = get_logger(__name__)

EXPIRATION_TIME_TO_SEC = 3_600  # 1 hour


class Api(BaseApi):
    """
    A class that implements sending GET request the HTML & XML markup of the
    https://rad.org.by/radiation.xml web resource.
    """

    _xml = urlparse(URL.RADIATION)
    _html = urlparse(URL.MONITORING)

    def __init__(self, url: str | None = None) -> None:
        """
        Instantiate a Api object.
        """
        self.url = url

    @timed_lru_cache(EXPIRATION_TIME_TO_SEC)
    def get_xml(self, uri: str | None = None) -> str | None:
        """
        A Method for getting XML markup of the web resource.
        """
        if not uri:
            response = self._get_markup(self._xml.geturl())
            return response.text if response else None
        response = self._get_markup(uri)
        return response.text if response else None

    @timed_lru_cache(EXPIRATION_TIME_TO_SEC)
    def get_html(self, uri: str | None = None) -> str | None:
        """
        A Method for getting HTML markup of the web resource.
        """
        if not uri:
            response = self._get_markup(self._html.geturl())
            return response.text if response else None
        response = self._get_markup(uri)
        return response.text if response else None

    def _get_markup(self, uri: str) -> requests.Response | None:
        """
        A Method for getting response on GET request to the web resource.
        """
        agent = UserAgent(
            browsers=[
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
        )
        try:
            with requests.session() as session:
                response = session.get(
                    uri,
                    verify=False,
                    headers={"User-Agent": agent.random},
                    timeout=(3, 7),
                )
        except requests.exceptions.RequestException as ex:
            logger.exception(
                "Unable to connect to the URL: %s. Raised exception: %s" % (uri, ex)
            )
            response = None

        if response and response.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED):
            return None

        return response
