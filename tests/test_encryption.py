import enum
from typing import TYPE_CHECKING, TypeAlias
from unittest import mock

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import ParameterSet
from cryptography.fernet import InvalidToken

from dosimeter.encryption import AsymmetricCryptographer, SymmetricCryptographer

if TYPE_CHECKING:
    from plugins.encryption import FilePaths, MessageAssertion, TokenAssertion

TokenType: TypeAlias = None | str | int | ParameterSet
MessageType: TypeAlias = None | str | int

ERROR_MSG = "invalid internal test config"


class TypeTokenValue(str, enum.Enum):
    """
    Enumeration of token value types.
    """

    UNDEFINED = "undefined"
    EMPTY = "empty"
    NUMBER = "number"
    INVALID = "invalid"

    def __str__(self) -> str:
        return self.value


class TypeMessageValue(str, enum.Enum):
    """
    Enumeration of message value types.
    """

    USERNAME = "username"
    PLAINTEXT = "plaintext"
    UNDEFINED = "undefined"
    EMPTY = "empty"
    NUMBER = "number"

    def __str__(self) -> str:
        return self.value


@pytest.fixture()
def get_token(
    request: SubRequest,
    fake_integer_number: int,
    fake_token: str,
) -> TokenType:
    """
    Generating token test data.
    """
    match request.param:
        case TypeTokenValue.UNDEFINED:
            return None
        case TypeTokenValue.EMPTY:
            return ""
        case TypeTokenValue.NUMBER:
            return fake_integer_number
        case TypeTokenValue.INVALID:
            return pytest.param(fake_token, marks=pytest.mark.xfail)
        case _:
            raise ValueError(ERROR_MSG)


@pytest.fixture()
def get_message(
    request: SubRequest,
    fake_username: str,
    fake_string: str,
    fake_integer_number: int,
) -> MessageType:
    """
    Generating message test data.
    """
    match request.param:
        case TypeMessageValue.USERNAME:
            return fake_username
        case TypeMessageValue.PLAINTEXT:
            return fake_string
        case TypeMessageValue.UNDEFINED:
            return None
        case TypeMessageValue.EMPTY:
            return ""
        case TypeMessageValue.NUMBER:
            return fake_integer_number
        case _:
            raise ValueError(ERROR_MSG)


@pytest.mark.encryption()
class TestSymmetricEncryption(object):
    """
    A class for testing the symmetric encryption logic.
    """

    cryptographer = SymmetricCryptographer()

    @pytest.mark.parametrize(
        "get_message",
        vals := list(TypeMessageValue),
        indirect=True,
        ids=[val + "_message" for val in vals],
    )
    def test_symmetric_encrypt(
        self,
        get_message: MessageType,
        assert_correct_token: "TokenAssertion",
    ) -> None:
        # Act
        token = self.cryptographer.encrypt(get_message)

        # Assert
        assert_correct_token(get_message, token)

    @pytest.mark.parametrize(
        "get_token",
        vals := list(TypeTokenValue),
        indirect=True,
        ids=[val + "_token" for val in vals],
    )
    def test_symmetric_decrypt_without_token(
        self,
        get_token: TokenType,
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Act
        message = self.cryptographer.decrypt(token=get_token)

        # Assert
        assert_correct_message(get_token, message)

    def test_symmetric_decrypt_with_invalid_token(self, fake_token: str) -> None:
        # Act
        with pytest.raises(InvalidToken) as exc_info:
            self.cryptographer.decrypt(token=fake_token)

        # Assert
        assert exc_info
        assert not str(exc_info.value)

    def test_symmetric_decrypt_with_valid_token(
        self,
        fake_string: str,
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Arrange
        token = self.cryptographer.encrypt(fake_string)

        # Act
        message = self.cryptographer.decrypt(token=token)

        # Assert
        assert_correct_message(token, message)


@pytest.mark.encryption()
class TestAsymmetricEncryption(object):
    """
    A class for testing the asymmetric encryption logic.
    """

    obj = "dosimeter.encryption.AsymmetricCryptographer"

    @pytest.mark.parametrize(
        "get_message",
        vals := list(TypeMessageValue),
        indirect=True,
        ids=[val + "_message" for val in vals],
    )
    def test_asymmetric_encrypt(
        self,
        get_keys: "FilePaths",
        get_message: MessageType,
        assert_correct_token: "TokenAssertion",
    ) -> None:
        # Arrange
        priv_key, pub_key, token_file = get_keys
        with mock.patch.multiple(self.obj, PRIV_KEY=priv_key, PUB_KEY=pub_key):
            cryptographer = AsymmetricCryptographer()

            # Act
            token = cryptographer.encrypt(get_message)

            # Assert
            assert_correct_token(get_message, token)

    @pytest.mark.parametrize(
        "get_token",
        vals := list(TypeTokenValue),
        indirect=True,
        ids=[val + "_token" for val in vals],
    )
    def test_asymmetric_decrypt_without_token(
        self,
        get_keys: "FilePaths",
        get_token: TokenType,
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Arrange
        priv_key, pub_key, token_file = get_keys
        with mock.patch.multiple(self.obj, PRIV_KEY=priv_key, PUB_KEY=pub_key):
            cryptographer = AsymmetricCryptographer()

            # Act
            message = cryptographer.decrypt(token=get_token)

            # Assert
            assert_correct_message(get_token, message)

    def test_asymmetric_decrypt_with_valid_token(
        self,
        get_keys: "FilePaths",
        fake_string: str,
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Arrange
        priv_key, pub_key, token_file = get_keys
        with mock.patch.multiple(self.obj, PRIV_KEY=priv_key, PUB_KEY=pub_key):
            cryptographer = AsymmetricCryptographer()
            token_file.write(cryptographer.encrypt(fake_string))
            token = token_file.read()

            # Act
            message = cryptographer.decrypt(token=token)

            # Assert
            assert_correct_message(token, message)
