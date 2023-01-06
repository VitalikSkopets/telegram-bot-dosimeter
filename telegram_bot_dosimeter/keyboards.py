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
    POINTS,
    SEND_LOCATION,
    TOTAL_COUNT_USERS,
    VITEBSK,
)

__all__ = (
    "main_keyboard",
    "points_keyboard",
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


def points_keyboard() -> ReplyKeyboardMarkup:
    """
    The menu monitoring points buttons to the user instead of the standard keyboard
    """
    keyboard = [
        [KeyboardButton(BREST.name)],
        [KeyboardButton(VITEBSK.name)],
        [KeyboardButton(GOMEL.name)],
        [KeyboardButton(GRODNO.name)],
        [KeyboardButton(MINSK.name)],
        [KeyboardButton(MOGILEV.name)],
        [KeyboardButton(MAIN_MENU.name)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    The admin inline menu buttons
    """
    keyboard = [
        [
            InlineKeyboardButton(
                TOTAL_COUNT_USERS.name, callback_data=TOTAL_COUNT_USERS.callback_data
            )
        ],
        [
            InlineKeyboardButton(
                LIST_ADMIN_IDS.name, callback_data=LIST_ADMIN_IDS.callback_data
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
