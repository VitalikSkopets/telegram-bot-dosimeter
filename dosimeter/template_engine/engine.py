import pathlib
from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from dosimeter.config import settings

__all__ = (
    "Template",
    "TemplateEngine",
)


@dataclass(frozen=True)
class Template:
    ADD_OR_DEL_USER: pathlib.Path = settings.TEMPLATES_DIR / "add_or_delete_user.html"
    ADMIN: pathlib.Path = settings.TEMPLATES_DIR / "admin.html"
    USER_COUNT: pathlib.Path = settings.TEMPLATES_DIR / "count_of_users.html"
    ADMIN_ERROR: pathlib.Path = settings.TEMPLATES_DIR / "error_to_admin.html"
    USER_ERROR: pathlib.Path = settings.TEMPLATES_DIR / "error_to_user.html"
    GREET: pathlib.Path = settings.TEMPLATES_DIR / "greeting.html"
    HELP: pathlib.Path = settings.TEMPLATES_DIR / "help.html"
    ADMINS_LIST: pathlib.Path = settings.TEMPLATES_DIR / "list_of_admins.html"
    LOCATION: pathlib.Path = settings.TEMPLATES_DIR / "location.html"
    MENU: pathlib.Path = settings.TEMPLATES_DIR / "menu.html"
    RADIATION: pathlib.Path = settings.TEMPLATES_DIR / "radiation.html"
    REGION: pathlib.Path = settings.TEMPLATES_DIR / "region.html"
    KEYBOARD: pathlib.Path = settings.TEMPLATES_DIR / "show_keyboard.html"
    START: pathlib.Path = settings.TEMPLATES_DIR / "start.html"
    TABLE: pathlib.Path = settings.TEMPLATES_DIR / "table.html"
    UNKNOWN: pathlib.Path = settings.TEMPLATES_DIR / "unknown.html"
    DONATE: pathlib.Path = settings.TEMPLATES_DIR / "donate.html"


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

    def render(self, file: pathlib.Path, **kwargs: Any) -> str:
        """
        This method will return the rendered template as a string.
        """
        template = self.env.get_template(file.name)
        return template.render(**kwargs)
