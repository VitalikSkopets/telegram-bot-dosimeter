from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from dosimeter.constants import Button

__all__ = (
    "admin_keyboard",
    "main_keyboard",
    "points_keyboard",
)


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    The function returns the menu buttons to the user instead of the standard keyboard.
    """
    keyboard = [
        [KeyboardButton(Button.MONITORING.label)],
        [KeyboardButton(Button.POINTS.label)],
        [KeyboardButton(Button.SEND_LOCATION.label, request_location=True)],
        [KeyboardButton(Button.HIDE_KEYBOARD.label)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def points_keyboard(button_list: tuple[Button, ...]) -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard.
    """
    keyboard = [
        [KeyboardButton(button_list[0].label)],
        [KeyboardButton(button_list[1].label)],
        [KeyboardButton(button.label) for button in button_list[2:4]],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    The admin inline menu buttons.
    """
    inline_button_list = (
        Button.TOTAL_COUNT_USERS,
        Button.LIST_ADMIN,
        Button.ADD_ADMIN,
        Button.DEL_ADMIN,
    )
    keyboard = [
        [InlineKeyboardButton(button.label, callback_data=button.callback_data)]
        for button in inline_button_list
    ]
    return InlineKeyboardMarkup(keyboard)


def donate_keyboard() -> InlineKeyboardMarkup:
    """
    The donate inline button.
    """
    keyboard = [[InlineKeyboardButton(Button.DONATE.label, url=Button.DONATE.url)]]
    return InlineKeyboardMarkup(keyboard)


def chart_keyboard() -> InlineKeyboardMarkup:
    """
    The show chart inline button.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                Button.SHOW_CHART.label, callback_data=Button.SHOW_CHART.callback_data
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
