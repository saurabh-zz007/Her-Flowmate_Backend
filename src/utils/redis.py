import redis.asyncio as redis
from redis.asyncio import Redis
from fastapi import Request

from src.utils.settings import settings

REDIS_CACHING_URL_SWITCHABLE = "redis://localhost:6379" if settings.REDIS_CACHING_URL is None else settings.REDIS_CACHING_URL

async def create_redis()->Redis:
    client = redis.from_url(
        REDIS_CACHING_URL_SWITCHABLE,
        decode_responses=True,
        max_connections=10,
        socket_connection_timeout=5,
        health_check_interval=30,
    )

    await client.ping()

    return client

def get_redis(request: Request) -> Redis:
    return request.app.state.redis
