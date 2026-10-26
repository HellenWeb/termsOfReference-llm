from aiogram.types import InlineKeyboardMarkup

# DELETE

balance = 0


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
                {
                    "text": f"Баланс: {balance}",
                },
            ],
        ]
    )
