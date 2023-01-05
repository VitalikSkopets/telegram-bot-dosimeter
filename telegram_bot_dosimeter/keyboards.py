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
    location_button = KeyboardButton(SEND_LOCATION.name, request_location=True)
    return ReplyKeyboardMarkup(
        [
            [MONITORING.name],
            [POINTS.name],
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
            [BREST.name],
            [VITEBSK.name],
            [GOMEL.name],
            [GRODNO.name],
            [MINSK.name],
            [MOGILEV.name],
            [MAIN_MENU.name],
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
                TOTAL_COUNT_USERS.name, callback_data=TOTAL_COUNT_USERS.callback_data
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
