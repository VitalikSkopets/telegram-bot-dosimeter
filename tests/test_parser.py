from pathlib import Path
from typing import TYPE_CHECKING, Callable
from unittest import mock

import httpretty
import pytest
from bs4 import BeautifulSoup

from dosimeter import config
from dosimeter.constants import Points, Regions
from dosimeter.parse.parser import Parser

if TYPE_CHECKING:
    from plugins.parsing import RegionInfoAssertion


def assign_id(val: str) -> str:
    """
    Generates string representations that are used in test IDs.
    """
    identifier = "{}_region"
    match val:
        case Regions.BREST:
            return identifier.format(Regions.BREST.name)
        case Regions.VITEBSK:
            return identifier.format(Regions.VITEBSK.name)
        case Regions.GOMEL:
            return identifier.format(Regions.GOMEL.name)
        case Regions.GRODNO:
            return identifier.format(Regions.GRODNO.name)
        case Regions.MOGILEV:
            return identifier.format(Regions.MOGILEV.name)
        case Regions.MINSK:
            return identifier.format(Regions.MINSK.name)


@pytest.mark.parsing()
class TestParser(object):
    """
    A class for testing logic encapsulated in the Parser class.
    """

    xml: Path = config.TESTS_DIR / "fixtures" / "rad.xml"
    html: Path = config.TESTS_DIR / "fixtures" / "rad.html"
    method = "dosimeter.parse.Parser._get_markup"

    @httpretty.activate
    def test_get_markup(self, get_text_from_file: Callable[[Path], str]) -> None:
        # Arrange
        httpretty.register_uri(
            method=httpretty.GET,
            uri=config.URL_RADIATION,
            body=get_text_from_file(self.xml),
            content_type="application/rss+xml",
        )

        # Act
        parser = Parser()
        response = parser._get_markup()

        # Assert
        assert httpretty.last_request().method == "GET"
        assert httpretty.last_request().path == "/radiation.xml"
        assert isinstance(response, BeautifulSoup)

    def test_get_points_with_radiation_level(
        self,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
    ) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = get_markup_from_file(self.xml)
            parser = Parser()
            result = parser.get_points_with_radiation_level()

        # Assert
        assert isinstance(result, dict)
        for key in result.keys():
            assert key in tuple(point.label for point in Points)
        for value in result.values():
            assert isinstance(value, float)
        mocked.assert_called_once()

    def test_get_mean_radiation_level(
        self,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
    ) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = get_markup_from_file(self.xml)
            parser = Parser()
            result = parser.get_mean_radiation_level()

        # Assert
        assert isinstance(result, float)
        assert 0 < result < 1
        assert round(result, 2) == 0.11
        mocked.assert_called_once()

    def test_get_info_about_radiation_monitoring(
        self,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
    ) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = get_markup_from_file(self.html)
            parser = Parser()
            result = parser.get_info_about_radiation_monitoring()

        # Assert
        assert isinstance(result, str)
        assert result.startswith("По состоянию")
        assert result.endswith("АЭС.")
        assert "на текущую дату радиационная" in result
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "get_points",
        vals := [region.value for region in Regions.__members__.values()],
        indirect=True,
        ids=assign_id,
    )
    def test_get_info_about_region(
        self,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
        get_points: tuple[Points],
        assert_correct_region_info: "RegionInfoAssertion",
    ) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = get_markup_from_file(self.xml)
            parser = Parser()
            result = parser.get_info_about_region(get_points)

        # Assert
        assert_correct_region_info(result, get_points)
        mocked.assert_called_once()
