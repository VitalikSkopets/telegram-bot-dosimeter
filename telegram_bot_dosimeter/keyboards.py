from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from telegram_bot_dosimeter.constants import Button, Command

__all__ = (
    "main_keyboard",
    "points_keyboard",
    "admin_keyboard",
)


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard
    """
    location_button = KeyboardButton(Button.SEND_LOCATION, request_location=True)
    return ReplyKeyboardMarkup(
        [
            [Button.MONITORING],
            [Button.POINTS],
            [location_button],
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


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    The admin inline menu buttons
    """
    keyboard = [
        [
            InlineKeyboardButton(
                Button.TOTAL_COUNT_USERS, callback_data=Command.TOTAL_COUNT_USERS
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
