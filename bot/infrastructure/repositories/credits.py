from sqlalchemy import select, text, update
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession
from bot.application.credits import InsufficientCreditsError
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
        try:
            await self._session.execute(text("BEGIN IMMEDIATE"))
            balance = await self._session.scalar(
                select(User.credits_balance).where(User.id == user_id)
            )
            if balance is None:
                raise LookupError(f"User {user_id} not found")
            inserted = await self._session.scalar(
                sqlite_insert(CreditTransaction)
                .values(
                    user_id=user_id,
                    amount=amount,
                    transaction_type=transaction_type,
                    idempotency_key=idempotency_key,
                )
                .on_conflict_do_nothing(index_elements=["idempotency_key"])
                .returning(CreditTransaction.id)
            )
            if inserted is None:
                await self._session.commit()
                return balance
            if balance + amount < 0:
                raise InsufficientCreditsError("Insufficient credits")

            new_balance = await self._session.scalar(
                update(User)
                .where(User.id == user_id)
                .values(credits_balance=User.credits_balance + amount)
                .returning(User.credits_balance)
            )
            await self._session.commit()
            return new_balance
        except Exception:
            await self._session.rollback()
            raise
    
