from pathlib import Path
from typing import Callable, TypeAlias

import pytest
from _pytest.fixtures import SubRequest
from bs4 import BeautifulSoup

from dosimeter.constants import Points, Regions
from dosimeter.parse.parser import ObservePoint, PowerOfRadiation

RegionInfoAssertion: TypeAlias = Callable[
    [tuple[list[tuple[ObservePoint, str]], PowerOfRadiation], tuple[Points, ...]], None
]


@pytest.fixture()
def get_markup_from_file() -> Callable[[Path], BeautifulSoup]:
    """
    Returns the BeautifulSoup object, which is a parsed html or xml document as a whole.
    """

    def factory(file_name: Path) -> BeautifulSoup:
        with open(file_name) as file:
            soup = BeautifulSoup(file, features="lxml-xml")
        return soup

    return factory


@pytest.fixture()
def get_text_from_file() -> Callable[[Path], str]:
    """
    Returns the plain text from xml format file.
    """

    def factory(file_name: Path) -> str:
        file = Path(file_name)
        return file.read_text()

    return factory


@pytest.fixture()
def get_points(request: SubRequest) -> tuple[Points, ...]:
    """
    Returns a tuple consisting of objects of monitoring points depending on the region.
    """
    match request.param:
        case Regions.BREST:
            return tuple(point for point in Points if point.region == Regions.BREST)
        case Regions.VITEBSK:
            return tuple(point for point in Points if point.region == Regions.VITEBSK)
        case Regions.GOMEL:
            return tuple(point for point in Points if point.region == Regions.GOMEL)
        case Regions.GRODNO:
            return tuple(point for point in Points if point.region == Regions.GRODNO)
        case Regions.MOGILEV:
            return tuple(point for point in Points if point.region == Regions.MOGILEV)
        case Regions.MINSK:
            return tuple(point for point in Points if point.region == Regions.MINSK)
        case _:
            raise ValueError("invalid internal test config")


@pytest.fixture()
def assert_correct_region_info() -> RegionInfoAssertion:
    """
    Assert that monitoring points and radiation doses values are correct.
    """

    def factory(
        result: tuple[list[tuple[ObservePoint, str]], PowerOfRadiation],
        region: tuple[Points, ...],
    ) -> None:
        assert isinstance(result, tuple)
        assert isinstance(result[0], list)
        assert isinstance(result[1], float)
        for label, value in result[0]:
            assert len(value) == 6
            assert isinstance(float(value.lstrip()), float)
            assert len(label) == 20
            assert label.rstrip("-") in tuple(point.label for point in region)

    return factory
