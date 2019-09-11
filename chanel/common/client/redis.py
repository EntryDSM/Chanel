from aioredis import Redis, create_redis_pool

from chanel.common.client.vault import settings


class RedisConnection:
    _redis: Redis = None

    @classmethod
    async def init(cls, connection_info) -> None:
        await cls.get_redis_pool(connection_info)

    @classmethod
    async def get_redis_pool(cls, connection_info) -> Redis:
        if not cls._redis or cls._redis.closed:
            cls._redis = await create_redis_pool(**connection_info)

        return cls._redis

    @classmethod
    async def destroy(cls) -> None:

        if cls._redis:
            cls._redis.close()
            await cls._redis.wait_closed()

        cls._redis = None

    @classmethod
    async def flush_all(cls) -> None:
        await cls._redis.flushall()

    @classmethod
    async def get(cls, key: str):
        redis_pool = await cls.get_redis_pool(settings.redis_connection_info)
        temp = await redis_pool.get(key)

        return temp if temp else None

    @classmethod
    async def set(cls, key: str, value: str, expire: int = None, pair: bool = False) -> None:
        redis_pool = await cls.get_redis_pool(settings.redis_connection_info)
        await redis_pool.set(key, value, expire=expire)

        if pair:
            await redis_pool.set(value, key, expire=expire)

    @classmethod
    async def delete(cls, key: str, pair: bool = False) -> None:
        redis_pool = await cls.get_redis_pool(settings.redis_connection_info)

        if pair:
            temp = await redis_pool.get(key)
            await redis_pool.delete(temp)

        await redis_pool.delete(key)
