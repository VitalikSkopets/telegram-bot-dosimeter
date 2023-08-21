import random
from typing import Callable, TypeAlias

import pytest
from mimesis import Field

from dosimeter.analytics import Event, Param, Payload
from dosimeter.constants import Action

PayloadDataAssertion: TypeAlias = Callable[[Payload], None]


@pytest.fixture()
def fake_locale(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random locale value.
    """
    return fake_field("code.locale_code")


@pytest.fixture()
def get_random_action() -> Action:
    """
    Getting random item value of the Action class.
    """
    return random.choice(list(Action))


@pytest.fixture()
def get_payload(
    fake_integer_number: int,
    fake_locale: str,
    get_random_action: Action,
    assert_correct_payload_data: PayloadDataAssertion,
) -> Payload:
    """
    Getting request parameters.
    """
    user_id = str(fake_integer_number)
    code = (
        fake_locale.split("-")[1].upper()
        if len(fake_locale) > 2
        else fake_locale.upper()
    )
    param = Param(language=code, engagement_time_msec=str(1))
    event = Event(name=get_random_action, params=param)
    payload = Payload(client_id=user_id, user_id=user_id, events=[event])
    assert_correct_payload_data(payload)

    return payload


@pytest.fixture()
def assert_correct_payload_data(
    fake_integer_number: int,
    get_random_action: Action,
) -> PayloadDataAssertion:
    """
    Assert that payload data values are correct.
    """

    def factory(payload: Payload) -> None:
        data = payload.dict()
        assert isinstance(payload, Payload)
        assert data["client_id"] == str(fake_integer_number)
        assert data["user_id"] == str(fake_integer_number)
        assert data["events"][0]["name"] == get_random_action
        assert len(data["events"][0]["params"]["language"]) == 2

    return factory
