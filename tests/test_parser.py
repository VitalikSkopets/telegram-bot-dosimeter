from pathlib import Path
from typing import TYPE_CHECKING, Callable
from unittest import mock

import pytest
from bs4 import BeautifulSoup

from dosimeter.config import config
from dosimeter.constants import URL, Point, Region
from dosimeter.parse.parser import Parser

if TYPE_CHECKING:
    from plugins.parsing import RegionInfoAssertion


def assign_id(val: str) -> str:
    """
    Generates string representations that are used in test IDs.
    """
    identifier = "{}_region"
    match val:
        case Region.BREST:
            return identifier.format(Region.BREST.name)
        case Region.VITEBSK:
            return identifier.format(Region.VITEBSK.name)
        case Region.GOMEL:
            return identifier.format(Region.GOMEL.name)
        case Region.GRODNO:
            return identifier.format(Region.GRODNO.name)
        case Region.MOGILEV:
            return identifier.format(Region.MOGILEV.name)
        case Region.MINSK:
            return identifier.format(Region.MINSK.name)


@pytest.mark.parsing()
class TestParser(object):
    """
    A class for testing logic encapsulated in the Parser class.
    """

    xml: Path = config.app.tests_dir / "fixtures" / "rad.xml"
    html: Path = config.app.tests_dir / "fixtures" / "rad.html"
    method = "dosimeter.parse.Parser._get_source"

    @pytest.mark.parametrize(
        "source,url",
        [
            (xml, URL.RADIATION),
            (html, URL.MONITORING),
        ],
        ids=["xml", "html"],
    )
    def test_get_source(
        self,
        source: Path,
        url: str,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
    ) -> None:
        # Act
        with mock.patch("dosimeter.api.external_api.Api._get_markup") as mocked:
            mocked.return_value = get_markup_from_file(source)
            parser = Parser()
            result = parser._get_source(url)

        # Assert
        assert isinstance(result, BeautifulSoup)
        mocked.assert_called_once()

    def test_get_xml_source(
        self,
        get_text_from_file: Callable[[Path], str],
    ) -> None:
        # Act
        with mock.patch.multiple(
            "dosimeter.api.external_api.Api",
            get_xml=mock.DEFAULT,
            get_html=mock.DEFAULT,
        ) as mocked:
            mocked["get_xml"].return_value = get_text_from_file(self.xml)
            mocked["get_html"].return_value = get_text_from_file(self.html)
            parser = Parser()
            result = parser._get_source(URL.RADIATION)

        # Assert
        assert isinstance(result, BeautifulSoup)
        mocked["get_xml"].assert_called_once()
        mocked["get_html"].assert_not_called()

    def test_get_html_source(
        self,
        get_text_from_file: Callable[[Path], str],
    ) -> None:
        # Act
        with mock.patch.multiple(
            "dosimeter.api.external_api.Api",
            get_html=mock.DEFAULT,
            get_xml=mock.DEFAULT,
        ) as mocked:
            mocked["get_html"].return_value = get_text_from_file(self.html)
            mocked["get_xml"].return_value = get_text_from_file(self.xml)
            parser = Parser()
            result = parser._get_source(URL.MONITORING)

        # Assert
        assert isinstance(result, BeautifulSoup)
        mocked["get_html"].assert_called_once()
        mocked["get_xml"].assert_not_called()

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
            assert key in tuple(point.label for point in Point)
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

    @pytest.mark.parametrize("region", list(Region), ids=assign_id)
    def test_get_info_about_region(
        self,
        region: Region,
        get_markup_from_file: Callable[[Path], BeautifulSoup],
        assert_correct_region_info: "RegionInfoAssertion",
    ) -> None:
        # Act
        with mock.patch(self.method) as mocked:
            mocked.return_value = get_markup_from_file(self.xml)
            parser = Parser()
            result = parser.get_region_info(region)

        # Assert
        assert_correct_region_info(result, region)
        mocked.assert_called_once()
