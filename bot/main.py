import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import get_settings
from bot.handlers.dialogue import router as dialogue_router
from bot.handlers.start import router as start_router
from bot.utils.logging import configure_logging

async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    storage = MemoryStorage()                    # ← обязательно
    bot = Bot(token=settings.bot_token.get_secret_value())
    dispatcher = Dispatcher(storage=storage)     # ← передаём storage

    dispatcher.include_routers(
        start_router,
        dialogue_router,
    )

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())