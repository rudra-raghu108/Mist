# app/core/redis.py
from redis import asyncio as aioredis
from app.core.config import settings

redis_client: aioredis.Redis | None = None


async def init_redis():
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )


async def close_redis():
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None
