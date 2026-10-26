from arq import Worker
from arq.connections import RedisSettings

from bot.config import get_settings
from bot.workers.context import shutdown, startup
from bot.workers.generation import generate_tz_task


class WorkerSettings:
    functions = [generate_tz_task]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_jobs = get_settings().worker_max_jobs
    job_timeout = get_settings().worker_job_timeout_seconds


if __name__ == "__main__":
    Worker(WorkerSettings).run()
