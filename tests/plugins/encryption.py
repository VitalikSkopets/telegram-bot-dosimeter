import random
from typing import Callable, TypeAlias

import pytest
from mimesis.schema import Field
from py.path import local

FilePaths: TypeAlias = tuple[local, local, local]
MessageAssertion: TypeAlias = Callable[[str, str], None]
TokenAssertion: TypeAlias = Callable[[str, str], None]


PLAINTEXT = "Test string"


@pytest.fixture(scope="class")
def get_keys(tmpdir_factory: pytest.TempdirFactory) -> FilePaths:
    """
    Generating temporary directory and files for testing encryption.
    """
    path_to_keys = tmpdir_factory.mktemp("keys")

    return (
        path_to_keys.join("secret.pem"),
        path_to_keys.join("public.pem"),
        path_to_keys.join("token.txt"),
    )


@pytest.fixture()
def _generate_encryption_test_data(
    request: pytest.FixtureRequest,
    fake_field: Field,
) -> None:
    """
    Generating data for testing encryption.
    """
    request.cls.token = (
        "Z0FBQUFBQmp5WVFSelUtaWdqRXN5MHdKenlGc1NYQ2RDYUctMTNtWC16UFdVRHhab2NGR2ljaFBhR"
        "2NKV1pUWTJKbVdyM21WblJFODM4VTMwWFdod1lNS3hnRWRlVENJbGc9PQ== "
    )
    request.cls.plaintext = PLAINTEXT
    request.cls.username = fake_field("person.username")
    request.cls.number = random.randrange(10_000_000)
    request.cls.empty = ""
    request.cls.undefined = None


@pytest.fixture()
def assert_correct_token() -> TokenAssertion:
    """
    Assert that token value is not equal message text.
    """

    def factory(message: str, token: str) -> None:
        if message and isinstance(message, str):
            assert isinstance(token, str)
            assert token != message
        if message is None or not isinstance(message, str):
            assert not token

    return factory


@pytest.fixture()
def assert_correct_message() -> MessageAssertion:
    """
    Assert that message value is valid.
    """

    def factory(token: str, message: str) -> None:
        if token and isinstance(token, str):
            assert isinstance(message, str)
            assert message == PLAINTEXT
        if token is None or not isinstance(token, str):
            assert not message

    return factory
