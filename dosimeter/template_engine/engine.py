import pathlib
from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from dosimeter.config import config

__all__ = (
    "Template",
    "TemplateEngine",
)


@dataclass(frozen=True)
class Template:
    ADD_OR_DEL_USER: pathlib.Path = config.app.templates_dir / "add_or_delete_user.html"
    ADMIN: pathlib.Path = config.app.templates_dir / "admin.html"
    USER_COUNT: pathlib.Path = config.app.templates_dir / "count_of_users.html"
    ADMIN_ERROR: pathlib.Path = config.app.templates_dir / "error_to_admin.html"
    USER_ERROR: pathlib.Path = config.app.templates_dir / "error_to_user.html"
    GREET: pathlib.Path = config.app.templates_dir / "greeting.html"
    HELP: pathlib.Path = config.app.templates_dir / "help.html"
    ADMINS_LIST: pathlib.Path = config.app.templates_dir / "list_of_admins.html"
    LOCATION: pathlib.Path = config.app.templates_dir / "location.html"
    MENU: pathlib.Path = config.app.templates_dir / "menu.html"
    RADIATION: pathlib.Path = config.app.templates_dir / "radiation.html"
    REGION: pathlib.Path = config.app.templates_dir / "region.html"
    KEYBOARD: pathlib.Path = config.app.templates_dir / "show_keyboard.html"
    START: pathlib.Path = config.app.templates_dir / "start.html"
    TABLE: pathlib.Path = config.app.templates_dir / "table.html"
    UNKNOWN: pathlib.Path = config.app.templates_dir / "unknown.html"
    DONATE: pathlib.Path = config.app.templates_dir / "donate.html"


class TemplateEngine:
    """
    Message template engine based on API to Jinja2.
    (see more https://jinja.palletsprojects.com/en/3.1.x/api/)
    """

    APP: str = config.app.name

    def __init__(self, templates_dir_name: str = config.app.templates_dir.stem) -> None:
        """
        Constructor method for initializing objects of class TemplateEngine.
        """
        self.templates = templates_dir_name
        self.env = Environment(
            loader=PackageLoader(self.APP, self.templates),
            autoescape=select_autoescape(),
        )

    def render(self, file: pathlib.Path, **kwargs: Any) -> str:
        """
        This method will return the rendered template as a string.
        """
        template = self.env.get_template(file.name)
        return template.render(**kwargs)
