from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from dosimeter.config import settings

__all__ = ("TemplateEngine",)


class TemplateEngine:
    """
    Message template engine based on API to Jinja2.
    (see more https://jinja.palletsprojects.com/en/3.1.x/api/)
    """

    APP: str = settings.APP

    def __init__(self, templates_dir_name: str = settings.TEMPLATES_DIR.stem) -> None:
        """
        Constructor method for initializing objects of class TemplateEngine.
        """
        self.templates = templates_dir_name
        self.env = Environment(
            loader=PackageLoader(self.APP, self.templates),
            autoescape=select_autoescape(),
        )

    def render(self, name: str, **kwargs: Any) -> str:
        """
        This method will return the rendered template as a string.
        """
        template = self.env.get_template(name)
        return template.render(**kwargs)
