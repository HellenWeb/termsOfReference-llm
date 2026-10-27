from bot.domain.enums import CreditTransactionType
from bot.domain.ports import CreditRepository
from bot.infrastructure.db.models import CreditTransaction, User
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import update


class InsufficientCreditsError(Exception):
    pass


class CreditService:
    def __init__(self, repository: CreditRepository) -> None:
        self._repository = repository

    async def balance(self, user_id: int) -> int:
        return await self._repository.get_balance(user_id)

    async def debit_generation(self, user_id: int, cost: int, task_id: str) -> int:
        balance = await self._repository.change_balance(
            user_id,
            -cost,
            CreditTransactionType.GENERATION_DEBIT,
            idempotency_key=f"generation:{task_id}",
        )
        if balance < 0:
            raise InsufficientCreditsError("Not enough credits")
        return balance

    async def grant(self, user_id: int, amount: int, transaction_type: CreditTransactionType, key: str) -> int:
        return await self._repository.change_balance(
            user_id, amount, transaction_type, idempotency_key=key
        )
    async def change_balance(self, user_id, amount, tx_type, *, idempotency_key) -> int:
        ins = await self._s.execute(
            pg_insert(CreditTransaction)
            .values(user_id=user_id, amount=amount,
                    transaction_type=tx_type, idempotency_key=idempotency_key)
            .on_conflict_do_nothing(index_elements=["idempotency_key"])
            .returning(CreditTransaction.id)
        )
        if ins.scalar_one_or_none() is None:      # повторный вызов
            return await self.get_balance(user_id)
        res = await self._s.execute(
            update(User)
            .where(User.id == user_id, User.credits_balance + amount >= 0)
            .values(credits_balance=User.credits_balance + amount)
            .returning(User.credits_balance)
        )
        balance = res.scalar_one_or_none()
        if balance is None:
            raise InsufficientCreditsError
        return balance
