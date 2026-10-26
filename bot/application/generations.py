from bot.domain.models import GenerationTaskData
from bot.domain.ports import GenerationTaskRepository, TaskQueue


class GenerationService:
    def __init__(self, repository: GenerationTaskRepository, queue: TaskQueue) -> None:
        self._repository = repository
        self._queue = queue

    async def submit(self, user_id: int, answers: dict[str, str]) -> GenerationTaskData:
        task = await self._repository.create(user_id, {"answers": answers})
        await self._queue.enqueue_generation(task.id)
        return task
