from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from telegram_bot_dosimeter.constants import (
    BREST,
    GOMEL,
    GRODNO,
    LIST_ADMIN_IDS,
    MAIN_MENU,
    MINSK,
    MOGILEV,
    MONITORING,
    NEXT,
    NEXT_ARROW,
    POINTS,
    PREV,
    PREV_ARROW,
    SEND_LOCATION,
    TOTAL_COUNT_USERS,
    VITEBSK,
)

__all__ = (
    "main_keyboard",
    "first_points_keyboard",
    "second_points_keyboard",
    "third_points_keyboard",
    "admin_keyboard",
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


def first_points_keyboard() -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    button_list = (
        BREST,
        VITEBSK,
        NEXT,
        MAIN_MENU,
    )
    keyboard = [[KeyboardButton(button.name)] for button in button_list]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def second_points_keyboard() -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    button_list = (
        GOMEL,
        GRODNO,
        PREV_ARROW,
        NEXT_ARROW,
    )
    keyboard = [[KeyboardButton(button.name)] for button in button_list]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def third_points_keyboard() -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    button_list = (
        MINSK,
        MOGILEV,
        PREV,
        MAIN_MENU,
    )
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
