import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config import get_settings
from bot.handlers.dialogue import router as dialogue_router
from bot.handlers.start import router as start_router
from bot.handlers.profile import router as profile_router
from bot.utils.logging import configure_logging
from bot.infrastructure.db.session import create_session_factory
from bot.middlewares.user import UserMiddleware
from bot.middlewares.db import DbSessionMiddleware
from bot.infrastructure.db.session import init_db

async def main() -> None:
    settings = get_settings()
    await init_db(settings)
    configure_logging(settings.log_level)
    session_factory = create_session_factory(settings)

    # storage = RedisStorage.from_url(settings.redis_url)
    bot = Bot(token=settings.bot_token.get_secret_value())
    dispatcher = Dispatcher()     # ← передаём storage

    dispatcher.update.middleware(DbSessionMiddleware(session_factory))
    dispatcher.update.middleware(UserMiddleware())

    dispatcher.include_routers(
        start_router,
        dialogue_router,
        profile_router
    )

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
