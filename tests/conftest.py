"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random
from string import ascii_letters, digits
from typing import Protocol, TypeVar, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

pytest_plugins = [
    "plugins.analytics",
    "plugins.encryption",
    "plugins.parsing",
    "plugins.storage",
]

T = TypeVar("T")
OPTION_LABEL = "randomly_seed"
MAX_LENGTH = 12


def pytest_configure(config: pytest.Config) -> None:
    """Read randomly seed from pytest config.

    Set it from cache if existed, set new if not and save to cache.
    """
    seed_length_in_bits = 32
    assert config.cache is not None
    seed_value = config.getoption(OPTION_LABEL)
    # random seed:
    default_seed = random.Random().getrandbits(seed_length_in_bits)

    match seed_value:
        case "last":
            seed = config.cache.get(OPTION_LABEL, default_seed)
        case "default":
            seed = default_seed
        case _:
            seed = seed_value

    # saving to cache
    cache = getattr(config, "cache", None)
    if cache is not None:
        config.cache.set(OPTION_LABEL, seed)
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


@pytest.fixture()
def fake_string(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random string value.
    """
    return fake_field("random.randstr", length=MAX_LENGTH)


@pytest.fixture()
def fake_integer_number(faker_seed: int, fake_field: Field) -> int:
    """
    Generating mimesis random integer number.
    """
    return fake_field("numeric.integer_number", start=1_000, end=1_000_000)


@pytest.fixture()
def fake_first_name(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random person first name.
    """
    return fake_field("person.first_name")


@pytest.fixture()
def fake_last_name(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random person last name.
    """
    return fake_field("person.last_name")


@pytest.fixture()
def fake_username(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random person username.
    """
    return fake_field("person.username")


@pytest.fixture()
def random_string() -> str:
    """
    Generating a random string of letters of different case and numbers without seed.
    """
    return "".join(random.choice(ascii_letters + digits) for _ in range(MAX_LENGTH))


@pytest.fixture()
def random_number() -> int:
    """
    Generating random integer value without seed.
    """
    return random.randrange(10_000_000)


@pytest.fixture()
def fake_url(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random url.
    """
    return fake_field("url")


@final
class FactoryListProtocol(Protocol[T]):
    """
    Makes list of objects
    """

    def __call__(self, count: int | None = 5) -> list[T]:
        """
        List of objects factory protocol.
        """
        ...
