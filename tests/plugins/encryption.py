from typing import Callable, TypeAlias

import pytest
from mimesis.schema import Field
from py.path import local

from dosimeter.config import config

FilePaths: TypeAlias = tuple[local, local, local]
MessageAssertion: TypeAlias = Callable[[str, str], None]
TokenAssertion: TypeAlias = Callable[[str, str], None]


@pytest.fixture(scope="class")
def get_keys(tmpdir_factory: pytest.TempdirFactory) -> FilePaths:
    """
    Generating temporary directory and files for testing encryption.
    """
    path_to_keys = tmpdir_factory.mktemp("keys")

    return (
        path_to_keys.join(config.enc.key.SECRET.name),
        path_to_keys.join(config.enc.key.PUBLIC.name),
        path_to_keys.join("token.txt"),
    )


@pytest.fixture()
def fake_token(faker_seed: int, fake_field: Field) -> str:
    """
    Generating mimesis random text string, in hexadecimal.
    """
    return fake_field("token_hex")


@pytest.fixture()
def assert_correct_token() -> TokenAssertion:
    """
    Assert that token value is not equal message text.
    """

    def factory(message: str | None, token: str) -> None:
        if message and isinstance(message, str):
            assert isinstance(token, str)
            assert token != message
        if message is None or not isinstance(message, str):
            assert not token

    return factory


@pytest.fixture()
def assert_correct_message(fake_string: str) -> MessageAssertion:
    """
    Assert that message value is valid.
    """

    def factory(token: str | None, message: str) -> None:
        if token and isinstance(token, str):
            assert isinstance(message, str)
            assert message == fake_string
        if token is None or not isinstance(token, str):
            assert not message

    return factory
