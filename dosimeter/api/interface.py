import abc

import requests


class BaseApi(abc.ABC):
    """
    A class that implements an interface for an external API.
    """

    @abc.abstractmethod
    def get_xml(self, uri: str | None = None) -> str | None:
        """
        A Method for getting XML markup of the web resource.
        """
        pass

    @abc.abstractmethod
    def get_html(self, uri: str | None = None) -> str | None:
        """
        A Method for getting HTML markup of the web resource.
        """
        pass

    @abc.abstractmethod
    def _get_markup(self, uri: str) -> requests.Response | None:
        """
        A method that makes a GET request to a resource and receives the HTML & XML
        markup of this web resource.
        """
        pass
