import json

from aioredis import Redis, create_redis_pool


class RedisConnection:
    redis: Redis = None

    @classmethod
    async def initialize(cls, connection_info):
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await create_redis_pool(**connection_info)

        return cls.redis

    @classmethod
    async def destroy(cls):
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    async def set(cls, key: str, value, expire: int = None) -> None:
        dumped_value = json.dumps(value)
        await cls.redis.set(key=key, value=dumped_value, expire=expire)

    @classmethod
    async def set_pair(cls, key: str, value: str, expire=None):
        await RedisConnection.set(key, value, expire)
        await RedisConnection.set(value, key, expire)

    @classmethod
    async def get(cls, key: str):
        temp_value = await cls.redis.get(key)
        return json.loads(temp_value) if temp_value else None

    @classmethod
    async def delete(cls, key: str) -> None:
        await cls.redis.delete(key)

    @classmethod
    async def delete_pair(cls, key: str) -> None:
        temp = await cls.get(key)
        await cls.delete(temp)
        await cls.delete(key)
