from ujson import dumps, loads
from aioredis import Redis, create_redis_pool


class RedisConnection:
    redis: Redis = None

    @classmethod
    async def initialize(cls, connection_info) -> Redis:

        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await create_redis_pool(**connection_info)

        return cls.redis

    @classmethod
    async def destroy(cls) -> None:

        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    async def set(cls, key: str, value: str, expire: int = None) -> None:
        await cls.redis.set(key=key, value=dumps(value), expire=expire)

    @classmethod
    async def set_pair(cls, key: str, value: str, expire: int = None) -> None:
        await cls.redis.set(key=key, value=dumps(value), expire=expire)
        await cls.redis.set(key=dumps(value), value=key, expire=expire)

    @classmethod
    async def get(cls, key: str):
        temp = await cls.redis.get(key)
        return loads(temp) if temp else None

    @classmethod
    async def delete(cls, key: str) -> None:
        await cls.redis.delete(key)

    @classmethod
    async def delete_pair(cls, key: str) -> None:
        temp = await cls.redis.get(key)
        await cls.redis.delete(temp)
        await cls.redis.delete(key)
