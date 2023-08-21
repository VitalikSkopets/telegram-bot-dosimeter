from http import HTTPStatus
from pathlib import Path
from typing import Callable
from unittest import mock

import httpretty
import pytest

from dosimeter.api import Api
from dosimeter.config import config
from dosimeter.constants import URL

testdata = [
    (
        URL.RADIATION,
        "<link>/monitoring/radiation.html</link>",
        "application/rss+xml",
        "/radiation.xml",
    ),
    (
        URL.MONITORING,
        '<link href="https://rad.org.by/monitoring/radiation" />',
        "text/html",
        "/monitoring/radiation",
    ),
]


@pytest.mark.api()
class TestApi(object):
    """
    A class for testing logic encapsulated in the Api class.
    """

    method = "dosimeter.api.external.Api._get_markup"

    @httpretty.activate
    def test_success_get_xml(self, get_text_from_file: Callable[[Path], str]) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=URL.RADIATION,
            body="<link>/monitoring/radiation.html</link>",
            status=HTTPStatus.OK,
            content_type="application/rss+xml",
        )

        # Act
        api = Api()
        response = api.get_xml()

        # Assert
        assert isinstance(response, str)
        assert response == "<link>/monitoring/radiation.html</link>"

    def test_fail_get_xml(self, get_text_from_file: Callable[[Path], str]) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = None
            api = Api()
            response = api.get_xml()

        # Assert
        assert not response
        mocked.assert_called_once()

    @httpretty.activate
    def test_success_get_html(self, get_text_from_file: Callable[[Path], str]) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=URL.MONITORING,
            body='<link href="https://rad.org.by/monitoring/radiation" />',
            status=HTTPStatus.OK,
            content_type="text/html",
        )

        # Act
        api = Api()
        response = api.get_html()

        # Assert
        assert isinstance(response, str)
        assert response == '<link href="https://rad.org.by/monitoring/radiation" />'

    @httpretty.activate
    def test_fail_get_html(self, get_text_from_file: Callable[[Path], str]) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = None
            api = Api()
            response = api.get_html()

        # Assert
        assert not response
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "url,body,content_type,path", testdata, ids=["xml", "html"]
    )
    @httpretty.activate
    def test_success_get_markup(
        self,
        url: str,
        body: str,
        content_type: str,
        path: str,
    ) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=url,
            body=body,
            status=HTTPStatus.OK,
            content_type=content_type,
        )

        # Act
        api = Api()
        response = api._get_markup(url)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.url == url
        assert response.text == body
        assert httpretty.last_request().method == "GET"
        assert httpretty.last_request().path == path

    @httpretty.activate
    def test_get_markup_none_response_with_fail_status_code(
        self,
        get_text_from_file: Callable[[Path], str],
    ) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=URL.RADIATION,
            body=get_text_from_file(config.app.tests_dir / "fixtures" / "rad.xml"),
            status=HTTPStatus.SERVICE_UNAVAILABLE,
            content_type="application/rss+xml",
        )

        # Act
        api = Api()
        response = api._get_markup(URL.RADIATION)

        # Assert
        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
        assert httpretty.last_request().method == "GET"
        assert httpretty.last_request().path == "/radiation.xml"
        assert not response

    @httpretty.activate
    def test_get_markup_none_response_with_fake_url(self, fake_url: str) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=fake_url,
            body=None,
        )

        # Act
        api = Api()
        response = api._get_markup(fake_url)

        # Assert
        assert httpretty.last_request().url == fake_url
        assert not httpretty.last_request().body
        assert not response
