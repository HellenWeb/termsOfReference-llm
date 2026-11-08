from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from bot.keyboards.inline import InlineForStartKeyboard
import html

router = Router(name=__name__)

@router.message(Command("start"))
async def start_handler(message):
    await message.answer(f"Здравствуйте <strong>{html.escape(message.from_user.first_name)}</strong> 🤙🫀!\n\nЭтот бот поможет вам написать грамотное техническое задание для вашего проекта. Чтобы начать проходить интервью, нажмите кнопку ниже. 🫰", reply_markup=InlineForStartKeyboard(), parse_mode="HTML")

@router.callback_query(F.data == "back")
async def back_start(callback: CallbackQuery):
    await callback.message.edit_text(f"Здравствуйте <strong>{html.escape(callback.from_user.first_name)}</strong> 🤙🫀!\n\nЭтот бот поможет вам написать грамотное техническое задание для вашего проекта. Чтобы начать проходить интервью, нажмите кнопку ниже. 🫰", reply_markup=InlineForStartKeyboard(), parse_mode="HTML")
    await callback.answer()

