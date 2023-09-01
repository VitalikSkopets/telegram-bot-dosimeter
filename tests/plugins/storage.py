import json
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from telegram import User
from typing_extensions import Unpack

from dosimeter.utils.file_manager import FileDataType

if TYPE_CHECKING:
    from conftest import FactoryListProtocol

FileDataFactory: TypeAlias = Callable[[Path], FileDataType]
TelegramUser: TypeAlias = Callable[[], User]
ListTelegramUsers: TypeAlias = Callable[[int | None], list[User]]


@final
class UserDTO(TypedDict, total=False):
    """Represent the user data.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    id: int
    first_name: str
    last_name: str
    username: str
    is_bot: bool


@final
class UserDTOFactory(Protocol):
    """
    Makes user data.
    """

    def __call__(self, **fields: Unpack[UserDTO]) -> UserDTO:
        """
        User data factory protocol.
        """
        return UserDTO(**fields)


@pytest.fixture()
def user_data_factory(
    fake_integer_number: int,
    fake_first_name: str,
    fake_username: str,
) -> UserDTOFactory:
    """
    Factory for fake random User Data Transfer Object.
    """

    def _factory(**fields: Unpack[UserDTO]) -> UserDTO:
        schema = Schema(
            schema=lambda: {
                "id": fake_integer_number,
                "first_name": fake_first_name,
                "last_name": None,
                "username": fake_username,
                "is_bot": False,
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[typeddict-item]
            **fields,
        }

    return _factory


@pytest.fixture()
def user_data(user_data_factory: UserDTOFactory) -> UserDTO:
    """
    Creates User Data Transfer Object for tests.
    """
    return user_data_factory()


@pytest.fixture()
def tgm_user_factory(user_data: UserDTO) -> TelegramUser:
    """
    Factory for generating fake Telegram User object base on User DTO.
    """

    def _create_tgm_user() -> User:
        return User(**user_data)

    return _create_tgm_user


@pytest.fixture()
def tgm_user(tgm_user_factory: TelegramUser) -> User:
    """
    Creates Telegram User object.
    """
    return tgm_user_factory()


@pytest.fixture()
def data_from_file_repo() -> FileDataFactory:
    """Factory for reading and returning data from a json file.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests
    """

    def _read_data_from_file(file_path: Path) -> FileDataType:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    return _read_data_from_file


@pytest.fixture()
def list_users_data_factory(faker_seed: int) -> "FactoryListProtocol[UserDTO]":
    """
    Factory for fake random List of User Data Transfer Objects.
    """

    def _make_list_user_dto(count: int | None = 5) -> list[UserDTO]:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                "id": mf("numeric.integer_number", start=1_000, end=1_000_000),
                "first_name": mf("person.first_name"),
                "last_name": mf("person.last_name"),
                "username": mf("person.username"),
                "is_bot": False,
            },
        )
        return schema.create(iterations=count)  # type: ignore[arg-type, return-value]

    return _make_list_user_dto


@pytest.fixture()
def list_tgm_users_factory(
    list_users_data_factory: "FactoryListProtocol[UserDTO]",
) -> ListTelegramUsers:
    """
    Factory for generating List of fake Telegram User objects.
    """

    def _make_list_tgm_users(count: int | None = 5) -> list[User]:
        return [User(**user_data) for user_data in list_users_data_factory(count)]

    return _make_list_tgm_users
