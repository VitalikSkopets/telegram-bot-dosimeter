import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from dosimeter import config
from dosimeter.cache import timed_lru_cache
from dosimeter.constants import Points
from dosimeter.messages import Message

__all__ = ("Parser", "parser")

logger = config.get_logger(__name__)

urllib3.disable_warnings()


class Parser:
    """A class that encapsulates the logic of parsing and scribing web pages."""

    URL_RADIATION: str = config.URL_RADIATION
    URL_MONITORING: str = config.URL_MONITORING

    def __init__(self, target: str | None = None) -> None:
        """Instantiate a Parser object"""
        self.url = target or self.URL_RADIATION

    @staticmethod
    def get_user_message(table: list[str], values: list[float]) -> str:
        """A static method for generating a response to the user in the form of a
        table with  radiation level values for each monitoring point."""
        line = Message.TABLE
        part_1 = line.format(config.TODAY, "Пункт наблюдения", "Мощность дозы")
        part_2 = "\n".join(table)
        line2 = Message.AVG
        part_3 = line2.format(sum(values) / len(values))
        return part_1 + part_2 + part_3

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
        """The method returns the float value of the average level of radiation."""
        soup = self._get_html()
        rad_level: list[str] = [val.text for val in soup.find_all("rad")]
        rad_level.reverse()
        mean_level = sum([float(level) for level in rad_level]) / len(rad_level)
        return mean_level

    def get_info_about_radiation_monitoring(self) -> str | None:
        """
        The method makes a GET request and scripts the html markup
        https://rad.org.by/monitoring/radiation.
        """
        markup = self._get_html(page=self.URL_MONITORING)
        lines = [span.text for span in markup.find_all("span")]
        data = Message.MONITORING
        cleaned_data = ""
        for line in lines:
            if line.startswith("По состоянию") and line.endswith("АЭС."):
                data = line.strip()
        if "натекущую датурадиационная" in data:
            cleaned_data = data.replace(
                "натекущую датурадиационная", "на текущую дату радиационная"
            )
        return cleaned_data or data

    def get_info_about_region(
        self, region: tuple[Points, ...]
    ) -> tuple[list[str], list[float]]:
        """
        The method calls the _get_html() private method, which sends a GET request
        and scripts the HTML markup of the https://rad.org.by/radiation.xml web
        resource. The results of scripting in the for loop are compared for equality
        with the names of the observation points located in the corresponding area,
        and together with the current date are substituted in the response message to
        the user.
        """
        line = "|<code>{}</code>|<code>{:^13}</code>|"
        values_by_region: list[float] = []
        table: list[str] = []

        for point, value in self.get_points_with_radiation_level():
            if point in [monitoring_point.label for monitoring_point in region]:
                values_by_region.append(float(value))
                table.append(line.format(self._format_string(point), value + " мкЗв/ч"))
        return table, values_by_region

    @timed_lru_cache(3600)
    def _get_html(self, page: str | None = None) -> BeautifulSoup | None:
        """Private method for scribing HTML markup of the web resource."""
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

    @staticmethod
    def _format_string(string: str, min_length: int = 20) -> str:
        """
        The method for increasing the length of the string object to 20 characters by
        filling in "-" spaces.
        """
        while len(string) < min_length:
            string += "-"
        return string


"""Parser class instance"""
parser = Parser()
