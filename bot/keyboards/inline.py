from aiogram.types import InlineKeyboardMarkup


def InlineForStartKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                {
                    "text": "🫦 Пройти интервью",
                    "callback_data": "start_interview"
                },
            ],
            [
                {
                    "text": "💞 MY </3",
                    "url": "https://hellenweb.github.io"
                },
                {
                    "text": "👁 Поддержка",
                    "url": "https://t.me/YungHellen"
                },
            ],
            [
                {
                    "text": "Профиль",
                    "callback_data": "profile"
                },
            ],
        ]
    )

def InlineForProfileKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                {
                    "text": "💳 Пополнить кредиты",
                    "callback_data": "top_up_credits"
                },
                {
                    "text": "🔙 Назад",
                    "callback_data": "back"
                },
            ]
        ]
    )