from arq import ArqRedis


class ArqTaskQueue:
    def __init__(self, redis: ArqRedis) -> None:
        self._redis = redis

    async def enqueue_generation(self, task_id: str) -> str:
        job = await self._redis.enqueue_job("generate_tz_task", task_id)
        if job is None:
            raise RuntimeError("Could not enqueue generation task")
        return job.job_id
