from unittest import mock

import pytest
import telegram

from dosimeter.config import config
from dosimeter.main import DosimeterBot, main


@pytest.mark.bot()
class TestDosimeterBot(object):
    """
    A class for testing logic encapsulated in the DosimeterBot class.
    """

    mocked = mock.create_autospec(DosimeterBot)

    def test_for_correct_instantiation_bot(self) -> None:
        # Act
        with pytest.raises(telegram.error.InvalidToken) as exc_info:
            bot = DosimeterBot("")
            assert not bot

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Invalid token"

    def test_unexpected_argument(self) -> None:
        # Act
        with pytest.raises(TypeError) as exc_info:
            self.mocked.start("unexpected argument")

        # Assert
        assert exc_info
        assert str(exc_info.value) == "too many positional arguments"

    def test_missing_attribute(self) -> None:
        # Act
        with pytest.raises(AttributeError) as exc_info:
            self.mocked.finish()

        # Assert
        assert exc_info
        assert str(exc_info.value) == "Mock object has no attribute 'finish'"

    def test_correct_signature(self):
        # Act
        checked = self.mocked.is_checked
        bot = self.mocked.start()

        # Assert
        assert checked
        assert bot

    @pytest.mark.skipif(
        config.app.webhook_mode is True,
        reason="activate webhook mode",
    )
    def test_start_bot_in_pooling_mode(self):
        # Act
        with mock.patch.multiple(
            "telegram.ext.updater.Updater",
            start_polling=mock.DEFAULT,
            start_webhook=mock.DEFAULT,
            idle=mock.DEFAULT,
        ) as mock_updater:
            bot = DosimeterBot(config.app.token)
            bot.start()

        # Assert
        assert isinstance(bot, DosimeterBot)
        mock_updater["start_polling"].assert_called_once()
        mock_updater["idle"].assert_called_once()
        mock_updater["start_webhook"].assert_not_called()

    @pytest.mark.skipif(
        config.app.webhook_mode is False,
        reason="deactivate webhook mode",
    )
    def test_start_bot_in_webhook_mode(self):
        # Arrange

        # Act
        with mock.patch.multiple(
            "telegram.ext.updater.Updater",
            start_polling=mock.DEFAULT,
            start_webhook=mock.DEFAULT,
            idle=mock.DEFAULT,
        ) as mock_updater:
            bot = DosimeterBot(config.app.token)
            bot.start()

        # Assert
        assert isinstance(bot, DosimeterBot)
        mock_updater["start_webhook"].assert_called_once()
        mock_updater["idle"].assert_called_once()
        mock_updater["start_polling"].assert_not_called()


@pytest.mark.bot()
class TestMainFunction(object):
    """
    A class for testing the main function.
    """

    bot_instance = "dosimeter.main.DosimeterBot"

    def test_main_func_with_success_check(self) -> None:
        # Act
        with mock.patch.multiple(
            self.bot_instance,
            is_checked=True,
            start=mock.DEFAULT,
        ) as mocked:
            main()

        # Assert
        mocked["start"].assert_called_once()

    def test_main_func_with_fail_check(self) -> None:
        # Act
        with mock.patch.multiple(
            self.bot_instance,
            is_checked=False,
            start=mock.DEFAULT,
        ) as mocked:
            main()

        # Assert
        mocked["start"].assert_not_called()
