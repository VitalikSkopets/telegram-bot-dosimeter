from unittest.mock import create_autospec

import pytest
from mimesis import Field

from dosimeter.constants import Point
from dosimeter.navigator import Navigator
from dosimeter.navigator.navigator import NearPoint


@pytest.fixture()
def fake_latitude(faker_seed: int, fake_field: Field) -> float:
    """
    Generating mimesis random latitude value.
    """
    return fake_field("address.latitude")


@pytest.fixture()
def fake_longitude(faker_seed: int, fake_field: Field) -> float:
    """
    Generating mimesis random longitude value.
    """
    return fake_field("address.longitude")


@pytest.mark.navigator()
class TestNavigator(object):

    mock = create_autospec(Navigator)
    navigator = Navigator()

    def test_missing_required_argument(self) -> None:
        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mock.get_near_point()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "missing a required argument: 'user_id'"

    def test_missing_attribute(self) -> None:
        # Act
        with pytest.raises(AttributeError) as exc_info:
            self.mock.get_further_point()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Mock object has no attribute 'get_further_point'"

    def test_correct_signature(
        self,
        fake_integer_number: int,
        fake_latitude: float,
        fake_longitude: float,
    ):
        # Arrange
        user_id = fake_integer_number

        # Act
        result = self.mock.get_near_point(
            user_id,
            latitude=fake_latitude,
            longitude=fake_longitude,
        )

        # Assert
        assert result

    def test_success(
        self,
        fake_integer_number: int,
        fake_latitude: float,
        fake_longitude: float,
    ):
        # Arrange
        user_id = fake_integer_number

        # Act
        result = self.navigator.get_near_point(
            user_id,
            latitude=fake_latitude,
            longitude=fake_longitude,
        )

        # Assert
        assert isinstance(result, NearPoint)
        assert isinstance(result.distance, float)
        assert isinstance(result.title, str)
        assert result.title in (point.label for point in Point)

    def test_success_with_default_coordinates(self, fake_integer_number: int):
        # Arrange
        user_id = fake_integer_number

        # Act
        result = self.navigator.get_near_point(user_id)

        # Assert
        assert isinstance(result, NearPoint)
        assert isinstance(result.distance, float)
        assert result.title == Point.OLTUSH.label
