import random

import pytest
from mimesis import Field

from dosimeter.analytics.measurement_protocol import Event, Param, Request
from dosimeter.constants import Action


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
def get_request_params(
    fake_integer_number: int,
    fake_locale: str,
    get_random_action: Action,
) -> Request:
    """
    Getting request parameters.
    """
    user_id = str(fake_integer_number)
    param = Param(language=fake_locale, engagement_time_msec=str(1))
    event = Event(name=get_random_action, params=param)
    return Request(client_id=user_id, user_id=user_id, events=[event])
