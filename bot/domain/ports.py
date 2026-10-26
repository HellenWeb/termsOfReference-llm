from datetime import UTC, datetime
from typing import Protocol

from bot.domain.enums import GenerationStatus
from bot.domain.models import GenerationTaskData


class UserRepository(Protocol):
    async def get_or_create(self, telegram_id: int, **profile: str | None) -> object: ...


class CreditRepository(Protocol):
    async def get_balance(self, user_id: int) -> int: ...

    async def change_balance(
        self,
        user_id: int,
        amount: int,
        transaction_type: str,
        *,
        idempotency_key: str,
    ) -> int: ...


class GenerationTaskRepository(Protocol):
    async def create(self, user_id: int, payload: dict) -> GenerationTaskData: ...

    async def set_status(
        self,
        task_id: str,
        status: GenerationStatus,
        *,
        error_message: str | None = None,
        result_url: str | None = None,
    ) -> None: ...


class TaskQueue(Protocol):
    async def enqueue_generation(self, task_id: str) -> str: ...


class Clock(Protocol):
    def now(self) -> datetime:
        return datetime.now(UTC)
