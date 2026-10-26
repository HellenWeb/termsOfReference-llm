from arq import ArqRedis, create_pool
from arq.connections import RedisSettings


async def create_redis_pool(redis_url: str) -> ArqRedis:
    return await create_pool(RedisSettings.from_dsn(redis_url))
