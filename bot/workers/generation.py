"""arq job functions; orchestration is intentionally a skeleton."""

from typing import Any


async def generate_tz_task(ctx: dict[str, Any], task_id: str) -> None:
    """Process one GenerationTask outside the Telegram polling process."""
    # TODO: mark PROCESSING, load answers, call LLM, create DOCX/PDF,
    # upload artifacts, mark COMPLETED, and notify the user via Bot API.
    _ = ctx, task_id


class WorkerSettings:
    """arq WorkerSettings configuration entry point."""

    functions = [generate_tz_task]
    on_startup = None
    on_shutdown = None

    # TODO: set redis_settings, max_jobs, job_timeout from application Settings.
