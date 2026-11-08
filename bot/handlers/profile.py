from aiogram import Router, F
from aiogram.filters import Command
from bot.infrastructure.repositories.credits import SqlAlchemyCreditRepository as CreditsRepository
from bot.keyboards.inline import InlineForProfileKeyboard
from bot.infrastructure.db.models import User

router = Router(name=__name__)

@router.message(Command("profile"))
async def profile_handler(message, user: User):
    await message.answer(
        f"Привет друг :)\n"
        f"Имя: {message.from_user.first_name}\n"
        f"Количество кредитов: {user.credits_balance}",
        reply_markup=InlineForProfileKeyboard()
    )

@router.callback_query(F.data == "profile")
async def profile_callback_handler(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        f"Привет друг :)\n"
        f"Имя: {callback.from_user.first_name}\n"
        f"Количество кредитов: {user.credits_balance}",
        reply_markup=InlineForProfileKeyboard()
    )
    await callback.answer()