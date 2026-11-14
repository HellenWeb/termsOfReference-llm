import html
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from bot.keyboards.inline import InlineForProfileKeyboard
from bot.infrastructure.db.models import User

router = Router(name=__name__)


def _profile_text(name: str, credits: int) -> str:
    return (
        "👤 <b>Профиль</b>\n"
        f"Привет, {html.escape(name)}!\n"
        f"💳 Кредитов: <b>{credits}</b>"
    )


@router.message(Command("profile"))
async def profile_handler(message: Message, user: User):
    await message.answer(
        _profile_text(message.from_user.first_name, user.credits_balance),
        parse_mode="HTML",
        reply_markup=InlineForProfileKeyboard()
    )

@router.callback_query(F.data == "profile")
async def profile_callback_handler(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        _profile_text(callback.from_user.first_name, user.credits_balance),
        parse_mode="HTML",
        reply_markup=InlineForProfileKeyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "top_up_credits")
async def top_up_credits_handler(callback: CallbackQuery):
    await callback.answer("Пополнение скоро будет доступно", show_alert=True)