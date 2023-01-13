from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from telegram_bot_dosimeter.constants import (
    LIST_ADMIN_IDS,
    MONITORING,
    POINTS,
    SEND_LOCATION,
    TOTAL_COUNT_USERS,
    Button,
)

__all__ = (
    "admin_keyboard",
    "main_keyboard",
    "points_keyboard",
)


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard
    """
    keyboard = [
        [KeyboardButton(MONITORING.name)],
        [KeyboardButton(POINTS.name)],
        [KeyboardButton(SEND_LOCATION.name, request_location=True)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def points_keyboard(button_list: tuple[Button, ...]) -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    keyboard = [[KeyboardButton(button.name)] for button in button_list]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    The admin inline menu buttons
    """
    inline_button_list = (TOTAL_COUNT_USERS, LIST_ADMIN_IDS)
    keyboard = [
        [InlineKeyboardButton(button.name, callback_data=button.callback_data)]
        for button in inline_button_list
    ]
    return InlineKeyboardMarkup(keyboard)
