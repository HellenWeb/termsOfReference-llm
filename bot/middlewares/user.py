from collections.abc import Awaitable, Callable
from typing import Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession
from bot.application.credits import CreditService
from bot.domain.enums import CreditTransactionType
from bot.config import get_settings
from bot.infrastructure.repositories.users import SqlAlchemyUserRepository
from bot.infrastructure.repositories.credits import SqlAlchemyCreditRepository


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession | None = data.get("session")
        tg_user: TgUser | None = data.get("event_from_user")

        if session is None or tg_user.is_bot:
          return await handler(event, data)
        
        user_repo = SqlAlchemyUserRepository(session)
        user, created = await user_repo.get_or_create(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name
        )

        if created:
            credit_repo = SqlAlchemyCreditRepository(session)
            credit_service = CreditService(credit_repo)
            await credit_service.grant(
                user_id=user.id,
                amount=100,
                transaction_type=CreditTransactionType.WELCOME,
                key=f"welcome_bonus:{user.id}"
            )
            await session.refresh(user)

        data["user"] = user

        return await handler(event, data)
    