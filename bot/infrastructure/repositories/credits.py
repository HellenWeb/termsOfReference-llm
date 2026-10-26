from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.domain.enums import CreditTransactionType
from bot.infrastructure.db.models import CreditTransaction, User


class SqlAlchemyCreditRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_balance(self, user_id: int) -> int:
        user = await self._session.get(User, user_id)
        if user is None:
            raise LookupError(f"User {user_id} not found")
        return user.credits_balance

    async def change_balance(
        self,
        user_id: int,
        amount: int,
        transaction_type: CreditTransactionType | str,
        *,
        idempotency_key: str,
    ) -> int:
        # TODO: execute SELECT ... FOR UPDATE and commit atomically.
        existing = await self._session.scalar(
            select(CreditTransaction).where(CreditTransaction.idempotency_key == idempotency_key)
        )
        if existing is not None:
            return await self.get_balance(user_id)
        user = await self._session.get(User, user_id)
        if user is None:
            raise LookupError(f"User {user_id} not found")
        if user.credits_balance + amount < 0:
            raise ValueError("Insufficient credits")
        user.credits_balance += amount
        self._session.add(
            CreditTransaction(
                user_id=user_id,
                amount=amount,
                transaction_type=transaction_type,
                idempotency_key=idempotency_key,
            )
        )
        await self._session.commit()
        return user.credits_balance
