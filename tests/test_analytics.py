from http import HTTPStatus
from unittest import mock

import httpretty
import pytest

from dosimeter.analytics import Analytics
from dosimeter.analytics.measurement_protocol import Request
from dosimeter.config import settings
from dosimeter.constants import Action


@pytest.mark.analytics()
class TestAnalytics(object):

    mocked = mock.create_autospec(Analytics)
    error_msg = "missing a required argument: '{arg}'"

    def test_missing_user_id_required_argument(self) -> None:
        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mocked.send()

        # Assert
        assert exc_info
        assert str(exc_info.value) == self.error_msg.format(arg="user_id")

    def test_missing_user_lang_code_required_argument(
        self,
        fake_integer_number: int,
    ) -> None:
        # Arrange
        user_id = fake_integer_number

        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mocked.send(user_id)

        # Assert
        assert exc_info
        assert str(exc_info.value) == self.error_msg.format(arg="user_lang_code")

    def test_missing_action_required_argument(
        self,
        fake_integer_number: int,
        fake_locale: str,
    ) -> None:
        # Arrange
        user_id = fake_integer_number
        user_lang_code = fake_locale

        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mocked.send(user_id, user_lang_code)

        # Assert
        assert exc_info
        assert str(exc_info.value) == self.error_msg.format(arg="action")

    def test_correct_signature(
        self,
        fake_integer_number: int,
        fake_locale: str,
        get_random_action: Action,
    ):
        # Arrange
        user_id = fake_integer_number
        user_lang_code = fake_locale
        action = get_random_action

        # Act
        result = self.mocked.send(user_id, user_lang_code, action)

        # Assert
        assert result

    def test_missing_attribute(self) -> None:
        # Act
        with pytest.raises(AttributeError) as exc_info:
            self.mocked.recieve()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Mock object has no attribute 'recieve'"

    def test_correct_method_call(
        self,
        fake_integer_number: int,
        fake_locale: str,
        get_random_action: Action,
        get_request_params: Request,
    ):
        # Act
        with mock.patch("requests.sessions.Session.post") as mocked:
            mocked.return_value = None
            analytics = Analytics()
            analytics.send(fake_integer_number, fake_locale, get_random_action)

        # Assert
        mocked.assert_called_once_with(analytics.url, json=get_request_params.dict())

    @httpretty.activate
    def test_success_send_request(
        self,
        fake_integer_number: int,
        fake_locale: str,
        get_random_action: Action,
        get_request_params: Request,
    ):
        # Arrange
        analytics = Analytics()

        httpretty.register_uri(
            method=httpretty.POST,
            uri=analytics.url,
            body=get_request_params.json(),
            status=HTTPStatus.OK,
            content_type="application/json",
        )

        # Act
        analytics.send(fake_integer_number, fake_locale, get_random_action)

        # Assert
        assert httpretty.has_request()
        assert httpretty.last_request().method == "POST"
        assert "/mp/collect?measurement_id=" in httpretty.last_request().path
        assert httpretty.last_request().body == bytes(
            get_request_params.json(), encoding=settings.UTF
        )
