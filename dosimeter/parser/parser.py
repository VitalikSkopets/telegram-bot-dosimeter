from dataclasses import dataclass
from statistics import mean
from typing import TypeAlias

from bs4 import BeautifulSoup, Tag

from dosimeter.api import BaseApi, api
from dosimeter.config.logger import get_logger
from dosimeter.constants import URL, Point, Region

logger = get_logger(__name__)

PowerOfRadiation: TypeAlias = float
ObservePoint: TypeAlias = str
NameOfRegion: TypeAlias = str


@dataclass
class RegionInfoDTO:
    """
    Class representing Data Transfer Object for region's information.
    """

    region: Region
    info: dict[ObservePoint, PowerOfRadiation]


class Parser(object):
    """
    A class that encapsulates the logic of parsing and scribing HTML & XML
    markup of the web resource.
    """

    def __init__(self, external_api: BaseApi = api) -> None:
        """
        Instantiate a Parser object.
        """
        self.api = external_api

    def get_points_with_radiation_level(
        self,
    ) -> dict[ObservePoint, PowerOfRadiation]:
        """
        The method returns a dictionary in which the keys are the names of radiation
        monitoring points, and the values of the keys are the power values
        of the equivalent radiation dose.
        """
        soup = self._get_source(URL.RADIATION)
        assert isinstance(soup, BeautifulSoup)
        points = [
            point.text
            for point in soup.find_all("title")
            if point.text != "Радиационный контроль и мониторинг"
        ]
        values = [float(value.text) for value in soup.find_all("rad")]
        return dict(zip(points, values))

    def get_mean_radiation_level(self) -> PowerOfRadiation:
        """
        The method returns the arithmetic mean of the radiation dose rate.
        """
        return mean(list(self.get_points_with_radiation_level().values()))

    def get_info_about_radiation_monitoring(self) -> str | None:
        """
        A method for parsing an object of the BeautifulSoup class, which is html markup
        https://rad.org.by/monitoring/radiation web resource.
        """
        soup = self._get_source(URL.MONITORING)
        assert isinstance(soup, BeautifulSoup)

        def has_substring(span: Tag) -> bool:
            return span.text.startswith("По состоянию")

        return (
            soup.find_all(has_substring)[0].text.replace("\xa0", " ").replace("  ", " ")
        )

    @staticmethod
    def draw_table(
        data: RegionInfoDTO,
    ) -> tuple[list[tuple[ObservePoint, str]], PowerOfRadiation]:
        """
        The method for parsing an object of the BeautifulSoup class, which is the XML
        markup web resource. Return the list of tuples containing the name of the
        monitoring point and the dose rate values, as well as the average dose rate
        value in the region.
        """
        values_by_region, table = [], []

        for point, value in data.info.items():
            values_by_region.append(value)
            table.append((point.ljust(20, "-"), "{:>6}".format(value)))

        return table, mean(values_by_region)

    def get_region_info(self, region: Region) -> RegionInfoDTO:
        """
        The method for parsing an object of the BeautifulSoup class, which is the XML
        markup web resource. Return the list of tuples containing the name of the
        monitoring point and the dose rate values, as well as the average dose rate
        value in the region.
        """
        points, values = [], []
        region_points = tuple(point for point in Point if point.region == region)

        for point, value in self.get_points_with_radiation_level().items():
            if point in [monitoring_point.label for monitoring_point in region_points]:
                points.append(point)
                values.append(value)

        return RegionInfoDTO(region=region, info=dict(zip(points, values)))

    def _get_source(self, url: str | None = None) -> BeautifulSoup | None:
        """
        Private method that calls API for getting HTML & XML markup of the web resource
        and return object of the BeautifulSoup class.
        """
        match url:
            case str() as uri if not uri.endswith(".xml"):
                markup = self.api.get_html(uri)
                formatter = "lxml"
            case _:
                markup = self.api.get_xml(url)
                formatter = "lxml-xml"
        return BeautifulSoup(markup, features=formatter) if markup else None
