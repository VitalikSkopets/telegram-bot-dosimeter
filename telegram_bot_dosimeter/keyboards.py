from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from telegram_bot_dosimeter.constants import Buttons

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
        [KeyboardButton(Buttons.MONITORING.label)],
        [KeyboardButton(Buttons.POINTS.label)],
        [KeyboardButton(Buttons.SEND_LOCATION.label, request_location=True)],
        [KeyboardButton(Buttons.HIDE_KEYBOARD.label)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def points_keyboard(button_list: list[Buttons]) -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    keyboard = [
        [KeyboardButton(button_list[0].label)],
        [KeyboardButton(button_list[1].label)],
        [KeyboardButton(button.label) for button in button_list[2:4]],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    The admin inline menu buttons
    """
    inline_button_list = (Buttons.TOTAL_COUNT_USERS, Buttons.LIST_ADMIN_IDS)
    keyboard = [
        [InlineKeyboardButton(button.label, callback_data=button.callback_data)]
        for button in inline_button_list
    ]
    return InlineKeyboardMarkup(keyboard)
