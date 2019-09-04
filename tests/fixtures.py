import pytest

from chanel.common.client.redis import RedisConnection


@pytest.fixture(scope="function")
async def redis_management(redis_DB, redis_proc):
    conn_info = {
        "address": f"redis://:@{redis_proc.host}:{redis_proc.port}",
        "minsize": 5,
        "maxsize": 10,
    }

    await RedisConnection.init(conn_info)
    await RedisConnection.flush_all()
    yield
    await RedisConnection.destroy()
