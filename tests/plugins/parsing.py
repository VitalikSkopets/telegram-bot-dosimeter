from pathlib import Path
from typing import Callable, TypeAlias

import pytest
from _pytest.fixtures import SubRequest
from bs4 import BeautifulSoup

from dosimeter.constants import Point, Region
from dosimeter.parse.parser import (
    NameOfRegion,
    ObservePoint,
    PowerOfRadiation,
    RegionInfoDTO,
)

RegionInfoAssertion: TypeAlias = Callable[[RegionInfoDTO, tuple[Point, ...]], None]


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
def get_points(request: SubRequest) -> tuple[tuple[Point, ...], Region]:
    """
    Returns a tuple consisting of objects of monitoring points depending on the region.
    """
    match request.param:
        case Region.BREST:
            return (
                tuple(point for point in Point if point.region == Region.BREST),
                Region.BREST,
            )
        case Region.VITEBSK:
            return (
                tuple(point for point in Point if point.region == Region.VITEBSK),
                Region.VITEBSK,
            )
        case Region.GOMEL:
            return (
                tuple(point for point in Point if point.region == Region.GOMEL),
                Region.GOMEL,
            )
        case Region.GRODNO:
            return (
                tuple(point for point in Point if point.region == Region.GRODNO),
                Region.GRODNO,
            )
        case Region.MOGILEV:
            return (
                tuple(point for point in Point if point.region == Region.MOGILEV),
                Region.MOGILEV,
            )
        case Region.MINSK:
            return (
                tuple(point for point in Point if point.region == Region.MINSK),
                Region.MINSK,
            )
        case _:
            raise ValueError("invalid internal test config")


@pytest.fixture()
def assert_correct_region_info() -> RegionInfoAssertion:
    """
    Assert that region, monitoring points, and radiation doses values are correct.
    """

    def factory(result: RegionInfoDTO, region: tuple[Point, ...]) -> None:
        assert isinstance(result, RegionInfoDTO)
        assert isinstance(result.region, NameOfRegion)
        assert result.region in list(Region)
        assert isinstance(result.info, dict)
        for label, value in result.info.items():
            assert isinstance(label, ObservePoint)
            assert label in tuple(point.label for point in region)
            assert isinstance(value, PowerOfRadiation)

    return factory
