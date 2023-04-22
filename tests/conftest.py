"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

pytest_plugins = [
    "plugins.encryption",
]


def pytest_configure(config: pytest.Config) -> None:
    """Read randomly seed from pytest config.

    Set it from cache if existed, set new if not and save to cache.
    """
    seed_length_in_bits = 32
    assert config.cache is not None
    seed_value = config.getoption("randomly_seed")
    # random seed:
    default_seed = random.Random().getrandbits(seed_length_in_bits)

    if seed_value == "last":
        seed = config.cache.get("randomly_seed", default_seed)
    elif seed_value == "default":
        seed = default_seed
    else:
        seed = seed_value

    # saving to cache
    cache = getattr(config, "cache", None)
    if cache is not None:
        config.cache.set("randomly_seed", seed)
    config.option.randomly_seed = seed


@pytest.fixture(scope="session", autouse=True)
def faker_seed(request: pytest.FixtureRequest) -> int:
    """
    Generating a random sequence of numbers.
    """
    return request.config.getoption("randomly_seed")


@pytest.fixture()
def fake_field(faker_seed: int) -> Field:
    """
    Generating mimesis field with fake data for RU locale.
    """
    return Field(locale=Locale.RU, seed=faker_seed)
