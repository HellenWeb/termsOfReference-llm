from bot.domain.enums import CreditTransactionType
from bot.domain.ports import CreditRepository


class InsufficientCreditsError(Exception):
    """Raised when a user cannot pay for a generation."""


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
