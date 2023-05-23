from unittest import mock

import pytest
import telegram

from dosimeter.config import settings
from dosimeter.main import DosimeterBot


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
        result = self.mocked.start()
        webhook_mode = self.mocked.WEBHOOK_MODE

        # Assert
        assert result
        assert isinstance(webhook_mode, bool)

    @pytest.mark.skipif(
        settings.WEBHOOK_MODE is True,
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
            bot = DosimeterBot(settings.TOKEN)
            bot.start()

        # Assert
        assert isinstance(bot, DosimeterBot)
        mock_updater["start_polling"].assert_called_once()
        mock_updater["idle"].assert_called_once()
        mock_updater["start_webhook"].assert_not_called()

    @pytest.mark.skipif(
        settings.WEBHOOK_MODE is False,
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
            bot = DosimeterBot(settings.TOKEN)
            bot.start()

        # Assert
        assert isinstance(bot, DosimeterBot)
        mock_updater["start_webhook"].assert_called_once()
        mock_updater["idle"].assert_called_once()
        mock_updater["start_polling"].assert_not_called()
