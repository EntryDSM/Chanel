import pytest
from aioredis.errors import RedisError

from chanel.repository.connections import RedisConnection

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cache_method, param",
    [
        ("set", {"key": "x", "value": {"y": 0}}),
        ("get", {"key": "x"}),
        ("delete", {"key": "x"}),
        ("flush_all", {}),
    ],
)
async def test_cache_connection_interface(cache_method, param, cache_manage):
    try:
        await getattr(RedisConnection, cache_method)(**param)
    except RedisError as e:
        assert (
            False
        )
