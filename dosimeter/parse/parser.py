from statistics import mean
from typing import TypeAlias

import requests
import urllib3
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent

from dosimeter import config
from dosimeter.cache import timed_lru_cache
from dosimeter.constants import Points

__all__ = ("ObservePoint", "Parser", "PowerOfRadiation")

logger = config.get_logger(__name__)

urllib3.disable_warnings()

PowerOfRadiation: TypeAlias = float
ObservePoint: TypeAlias = str


class Parser:
    """
    A class that encapsulates the logic of parsing and scribing web pages.
    """

    URL_RADIATION: str = config.URL_RADIATION
    URL_MONITORING: str = config.URL_MONITORING

    def __init__(self, target: str | None = None) -> None:
        """
        Instantiate a Parser object.
        """
        self.url = target or self.URL_RADIATION

    def get_points_with_radiation_level(
        self,
    ) -> dict[ObservePoint, PowerOfRadiation]:
        """
        The method returns a dictionary in which the keys are the names of radiation
        monitoring points, and the values of the keys are the power values
        of the equivalent radiation dose.
        """
        soup = self._get_markup()
        points = [
            point.text
            for point in soup.find_all("title")
            if point.text != "Радиационный контроль и мониторинг"
        ]
        values = [float(value.text) for value in soup.find_all("rad")]
        return dict(zip(points, values))

    def get_mean_radiation_level(self) -> PowerOfRadiation:
        """
        Returns the arithmetic mean of the radiation dose rate.
        """
        return mean(list(self.get_points_with_radiation_level().values()))

    def get_info_about_radiation_monitoring(self) -> str | None:
        """
        The method makes a GET request and scripts the html markup
        https://rad.org.by/monitoring/radiation.
        """
        markup = self._get_markup(page=self.URL_MONITORING)

        def has_substring(span: Tag) -> bool:
            return span.text.startswith("По состоянию")

        data = markup.find_all(has_substring)[0].text
        if "натекущую датурадиационная" in data:
            data = data.replace(
                "натекущую датурадиационная", "на текущую дату радиационная"
            )
        return data

    def get_info_about_region(
        self, region: tuple[Points, ...]
    ) -> tuple[list[tuple[ObservePoint, str]], PowerOfRadiation]:
        """
        The method calls the _get_markup() private method, which sends a GET request
        and scripts the HTML/XML markup of the https://rad.org.by/radiation.xml web
        resource. Return value: list of tuples containing the name of the
        monitoring point and the dose rate values, as well as the average
        dose rate value in the region.
        """
        values_by_region = []
        table = []

        for point, value in self.get_points_with_radiation_level().items():
            if point in [monitoring_point.label for monitoring_point in region]:
                values_by_region.append(value)
                table.append((point.ljust(20, "-"), "{:>6}".format(value)))

        return table, mean(values_by_region)

    @timed_lru_cache(3_600)
    def _get_markup(self, page: str | None = None) -> BeautifulSoup | None:
        """
        Private method for scribing HTML & XML markup of the web resource.
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
        response = None
        try:
            response = requests.get(
                page or self.url, verify=False, headers={"User-Agent": agent.random}
            )
        except Exception as ex:
            logger.exception(
                "Unable to connect to the URL: %s. Raised exception: %s"
                % (page or self.url, ex)
            )

        soup = BeautifulSoup(response.text, features="lxml-xml") if response else None
        return soup
