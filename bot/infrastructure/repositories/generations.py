from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from bot.domain.enums import GenerationStatus
from bot.domain.models import GenerationTaskData
from bot.infrastructure.db.models import GenerationTask


class SqlAlchemyGenerationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: int, payload: dict) -> GenerationTaskData:
        task = GenerationTask(user_id=user_id, input_payload=payload)
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return GenerationTaskData(id=str(task.id), user_id=user_id, status=task.status, created_at=task.created_at)

    async def set_status(
        self,
        task_id: str,
        status: GenerationStatus,
        *,
        error_message: str | None = None,
        result_url: str | None = None,
    ) -> None:
        task = await self._session.get(GenerationTask, UUID(task_id))
        if task is None:
            raise LookupError(f"Generation task {task_id} not found")
        task.status = status
        task.error_message = error_message
        task.result_url = result_url
        await self._session.commit()
