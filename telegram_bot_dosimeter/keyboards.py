from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram_bot_dosimeter.constants import Button

__all__ = (
    "main_keyboard",
    "points_keyboard",
)


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard
    """
    location_keyboard = KeyboardButton(Button.SEND_LOCATION, request_location=True)
    return ReplyKeyboardMarkup(
        [
            [Button.MONITORING],
            [Button.POINTS],
            [location_keyboard],
        ],
        resize_keyboard=True,
    )


def points_keyboard() -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    return ReplyKeyboardMarkup(
        [
            [Button.BREST],
            [Button.VITEBSK],
            [Button.GOMEL],
            [Button.GRODNO],
            [Button.MINSK],
            [Button.MOGILEV],
            [Button.MAIN_MENU],
        ],
        resize_keyboard=True,
    )
