import pathlib
from unittest import mock

import jinja2
import pytest

from dosimeter.template_engine import Template, TemplateEngine


@pytest.fixture(scope="session")
def message_engine() -> TemplateEngine:
    """
    Create TemplateEngine class instance.
    """
    return TemplateEngine()


@pytest.mark.message_engine()
class TestMessageEngine(object):
    """
    A class for testing the message template rendering.
    """

    template: pathlib.Path = Template.HELP

    def test_render_message_with_template_render_mock(
        self,
        message_engine: TemplateEngine,
    ) -> None:
        # Act
        with mock.patch(
            "jinja2.environment.Template.render",
            return_value="Jinja render success",
        ) as mocked:
            rendered_message = message_engine.render(self.template)

        # Assert
        assert isinstance(rendered_message, str)
        assert rendered_message == mocked.return_value
        mocked.assert_called_once()

    def test_render_message_with_template_engine_render_mock(
        self,
        message_engine: TemplateEngine,
    ) -> None:
        # Act
        with mock.patch(
            "dosimeter.template_engine.engine.TemplateEngine.render",
            return_value=f"Render success '{self.template}' template",
        ) as mocked:
            rendered_message = message_engine.render(self.template)

        # Assert
        assert isinstance(rendered_message, str)
        assert rendered_message == mocked.return_value
        mocked.assert_called_once_with(self.template)

    def test_success_message_render(
        self,
        message_engine: TemplateEngine,
    ) -> None:
        # Act
        rendered_message = message_engine.render(self.template)

        # Assert
        assert isinstance(rendered_message, str)
        assert "1 Зиверт = 100 Рентген" in rendered_message

    def test_fail_message_render_without_template(
        self,
        message_engine: TemplateEngine,
    ) -> None:
        # Act
        with pytest.raises(jinja2.exceptions.TemplateNotFound) as exc_info:
            message_engine.render(pathlib.Path(""))

        # Assert
        assert exc_info
        assert not str(exc_info.value)
