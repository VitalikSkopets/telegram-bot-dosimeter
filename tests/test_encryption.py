# type: ignore[attr-defined]
from typing import TYPE_CHECKING, Any
from unittest import mock

import pytest

from dosimeter.encryption import AsymmetricCryptographer, SymmetricCryptographer

if TYPE_CHECKING:
    from plugins.encryption import FilePaths, MessageAssertion, TokenAssertion


@pytest.mark.usefixtures("_generate_encryption_test_data")
class TestMiddlewareEncryption(object):
    """
    A class with common methods for testing the encryption logic.
    """

    def create_messages(self) -> tuple[Any, ...]:
        return (
            self.username,
            self.plaintext,
            self.undefined,
            self.empty,
            self.number,
        )

    def create_tokens(self) -> tuple[str, None, int]:
        return self.token, self.undefined, self.number


@pytest.mark.encryption()
@pytest.mark.usefixtures("_generate_encryption_test_data")
class TestSymmetricEncryption(TestMiddlewareEncryption):
    """
    A class for testing the symmetric encryption logic.
    """

    cryptographer = SymmetricCryptographer()

    def test_symmetric_encrypt(
        self,
        assert_correct_token: "TokenAssertion",
    ) -> None:
        # Act
        for message in self.create_messages():
            token = self.cryptographer.encrypt(message)

            # Assert
            assert_correct_token(message, token)

    def test_symmetric_decrypt(
        self,
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Act
        for token in self.create_tokens():
            message = self.cryptographer.decrypt(token=token)

            # Assert
            assert_correct_message(token, message)


@pytest.mark.encryption()
@pytest.mark.usefixtures("_generate_encryption_test_data")
class TestAsymmetricEncryption(TestMiddlewareEncryption):
    """
    A class for testing the asymmetric encryption logic.
    """

    def test_asymmetric_encrypt(
        self,
        get_keys: "FilePaths",
        assert_correct_token: "TokenAssertion",
    ) -> None:
        # Arrange
        priv_key, pub_key, token_file = get_keys
        with mock.patch.multiple(
            "dosimeter.encryption.AsymmetricCryptographer",
            PRIV_KEY_PATH=priv_key,
            PUB_KEY_PATH=pub_key,
        ):
            cryptographer = AsymmetricCryptographer()

            # Act
            for message in self.create_messages():
                token = cryptographer.encrypt(message)

                # Assert
                assert_correct_token(message, token)

    def test_asymmetric_decrypt(
        self,
        get_keys: "FilePaths",
        assert_correct_message: "MessageAssertion",
    ) -> None:
        # Arrange
        priv_key, pub_key, token_file = get_keys
        with mock.patch.multiple(
            "dosimeter.encryption.AsymmetricCryptographer",
            PRIV_KEY_PATH=priv_key,
            PUB_KEY_PATH=pub_key,
        ):
            cryptographer = AsymmetricCryptographer()
            token_file.write(cryptographer.encrypt(self.plaintext))
            token = token_file.read()

            # Act
            for token in (self.undefined, self.number, token):
                message = cryptographer.decrypt(token=token)

                # Assert
                assert_correct_message(token, message)
