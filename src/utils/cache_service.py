from redis.asyncio import Redis
import json
from fastapi.encoders import jsonable_encoder

class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        value = await self.redis.get(key)

        if value is None:
            return None
        
        return json.loads(value)
    
    async def set(
            self,
            key: str,
            value,
            ttl: int = 600
    ):
        json_value = jsonable_encoder(value)
        await self.redis.set(
            key,
            json.dumps(json_value),
            ex=ttl
        )

    async def delete(self, key:str):
        await self.redis.delete(key)

    async def exists(self, key:str):
        exist = await self.redis.exists(key)
        return exist
