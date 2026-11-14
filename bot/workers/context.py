from dataclasses import dataclass
from arq.connections import RedisSettings
from bot.config import Settings
from functools import lru_cache


@dataclass(slots=True)
class WorkerContext:
    settings: Settings
    # TODO: add SQLAlchemy session factory and object storage client.
    SQLAlcheySession: Any
    ObjectStorageClient: Any


async def startup(ctx: dict) -> None:
    settings = Settings()
    ctx["dependencies"] = WorkerContext(settings=settings)


async def shutdown(ctx: dict) -> None:
    # TODO: close DB, HTTP, and object-storage clients.
    ctx.pop("dependencies", None)

@lru_cache(maxsize=1)
async def get_settings(ctx: dict) -> Settings:
    return ctx["dependencies"].settings
