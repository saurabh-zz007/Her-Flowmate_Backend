import redis.asyncio as redis
from redis.asyncio import Redis
from fastapi import Request

from src.utils.settings import settings
from src.utils.cache_service import CacheService

REDIS_CACHING_URL_SWITCHABLE = settings.REDIS_CACHING_URL

async def create_redis()->Redis:
    client = redis.from_url(
        REDIS_CACHING_URL_SWITCHABLE,
        decode_responses=True,
        max_connections=10,
        socket_connect_timeout=5,
        health_check_interval=30,
    )

    await client.ping()

    return client

def get_redis(request: Request) -> CacheService:
    raw_redis = request.app.state.redis
    return CacheService(raw_redis)
