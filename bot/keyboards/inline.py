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
                }
            ]
        ]
        
    )
