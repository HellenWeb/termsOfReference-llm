from aiogram import Router
from aiogram.filters import Command
from bot.keyboards.inline import InlineForStartKeyboard

router = Router(name=__name__)

@router.message(Command("start"))
async def start_handler(message):
    await message.answer(f"Здравствуйте! {message.from_user.first_name}, этот бот поможет вам написать грамотное техническое задание для вашего проекта. Чтобы начать, нажмите кнопку ниже.", reply_markup=InlineForStartKeyboard())

# TODO: implement the /start handler and introduce users to the dialogue.
