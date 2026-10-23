from aiogram import Router
from aiogram.filters import Command
from bot.keyboards.inline import InlineForStartKeyboard

router = Router(name=__name__)

@router.message(Command("start"))
async def start_handler(message):
    await message.answer(f"Здравствуйте <strong>{message.from_user.first_name}</strong> 🤙🫀!\n\nЭтот бот поможет вам написать грамотное техническое задание для вашего проекта. Чтобы начать проходить интервью, нажмите кнопку ниже. 🫰", reply_markup=InlineForStartKeyboard(), parse_mode="HTML")

