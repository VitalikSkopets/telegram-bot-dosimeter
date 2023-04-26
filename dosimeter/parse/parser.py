import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from dosimeter import config
from dosimeter.cache import timed_lru_cache
from dosimeter.constants import Points

__all__ = ("Parser",)

logger = config.get_logger(__name__)

urllib3.disable_warnings()


class Parser:
    """A class that encapsulates the logic of parsing and scribing web pages."""

    URL_RADIATION: str = config.URL_RADIATION
    URL_MONITORING: str = config.URL_MONITORING

    def __init__(self, target: str | None = None) -> None:
        """Instantiate a Parser object"""
        self.url = target or self.URL_RADIATION

    def get_points_with_radiation_level(self) -> list[tuple[str, str]]:
        """
        The method returns a list of tuples with the names of radiation monitoring
        points and values of the equivalent dose rate of gamma radiation.
        """
        soup = self._get_html()
        points: list[str] = [point.text for point in soup.find_all("title")]
        points.reverse()
        values: list[str] = [value.text for value in soup.find_all("rad")]
        values.reverse()
        return list(zip(points, values))

    def get_avg_radiation_level(self) -> float:
        """
        The method returns the float value of the average level of radiation.
        """
        soup = self._get_html()
        rad_level: list[str] = [val.text for val in soup.find_all("rad")]
        rad_level.reverse()
        return sum([float(level) for level in rad_level]) / len(rad_level)

    def get_info_about_radiation_monitoring(self) -> str | None:
        """
        The method makes a GET request and scripts the html markup
        https://rad.org.by/monitoring/radiation.
        """
        markup = self._get_html(page=self.URL_MONITORING)
        lines = [span.text for span in markup.find_all("span")]
        data = ""
        for line in lines:
            if line.startswith("По состоянию") and line.endswith("АЭС."):
                data = line.strip()
        if "натекущую датурадиационная" in data:
            data = data.replace(
                "натекущую датурадиационная", "на текущую дату радиационная"
            )
        return data

    def get_info_about_region(
        self, region: tuple[Points, ...]
    ) -> tuple[list[tuple[str, str]], float]:
        """
        The method calls the _get_html() private method, which sends a GET request
        and scripts the HTML markup of the https://rad.org.by/radiation.xml web
        resource. Return value: list of tuples containing the name of the
        monitoring point and the dose rate values, as well as the average
        dose rate value in the region.
        """
        values_by_region: list[float] = []
        table: list[tuple[str, str]] = []

        for point, value in self.get_points_with_radiation_level():
            if point in [monitoring_point.label for monitoring_point in region]:
                values_by_region.append(float(value))
                table.append((point.ljust(20, "-"), "{:>6}".format(value)))

        mean_value = sum(values_by_region) / len(values_by_region)
        return table, mean_value

    @timed_lru_cache(3600)
    def _get_html(self, page: str | None = None) -> BeautifulSoup | None:
        """
        Private method for scribing HTML markup of the web resource.
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
