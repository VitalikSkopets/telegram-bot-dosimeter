from pathlib import Path
from typing import Callable, TypeAlias

import pytest
from bs4 import BeautifulSoup

from dosimeter.constants import Point, Region
from dosimeter.parser import NameOfRegion, ObservePoint, PowerOfRadiation, RegionInfoDTO

RegionInfoAssertion: TypeAlias = Callable[[RegionInfoDTO, Region], None]


def assign_id(fixture_value: str) -> str:
    """
    Generates string representations that are used in test IDs.
    """
    string_ids = "{name}_region"
    identifiers = {
        Region.BREST.value: string_ids.format(name=Region.BREST.name),
        Region.VITEBSK.value: string_ids.format(name=Region.VITEBSK.name),
        Region.GOMEL.value: string_ids.format(name=Region.GOMEL.name),
        Region.GRODNO.value: string_ids.format(name=Region.GRODNO.name),
        Region.MOGILEV.value: string_ids.format(name=Region.MOGILEV.name),
        Region.MINSK.value: string_ids.format(name=Region.MINSK.name),
    }

    return identifiers[fixture_value]


@pytest.fixture()
def get_markup_from_file() -> Callable[[Path], BeautifulSoup]:
    """
    Returns the BeautifulSoup object, which is a parsed html or xml document as a whole.
    """

    def factory(file_name: Path) -> BeautifulSoup:
        with open(file_name) as file:
            formatter = "lxml-xml" if file_name.suffix == ".xml" else "lxml"
            soup = BeautifulSoup(file, features=formatter)
        return soup

    return factory


@pytest.fixture()
def get_text_from_file() -> Callable[[Path], str]:
    """
    Returns the plain text from html & xml format file.
    """

    def factory(file_name: Path) -> str:
        file = Path(file_name)
        return file.read_text()

    return factory


@pytest.fixture()
def assert_correct_region_info() -> RegionInfoAssertion:
    """
    Assert that region, monitoring points, and radiation doses values are correct.
    """

    def factory(result: RegionInfoDTO, region: Region) -> None:
        assert isinstance(result, RegionInfoDTO)
        assert isinstance(result.region, NameOfRegion)
        assert result.region in list(Region)
        assert result.region == region
        assert isinstance(result.info, dict)
        for label, value in result.info.items():
            assert isinstance(label, ObservePoint)
            assert label in [point.label for point in Point if point.region == region]
            assert isinstance(value, PowerOfRadiation)

    return factory
