
from aiogram.types import InlineKeyboardMarkup


def InlineForStartKeyboard() -> InlineKeyboardMarkup:
    """Create an inline keyboard for the /start command."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                {
                    "text": "💞 MY </3",
                    "url": "https://hellenweb.github.io"
                },
                {
                    "text": "Пройти интервью",
                    "callback_data": "start_interview"
                },
                {
                    "text": "Поддержка",
                    "url": "https://t.me/YungHellen"
                }
            ]
        ]
    )
