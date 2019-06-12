import sanic

from chanel.config.setting import settings
from chanel.repository.connections import RedisConnection


async def initialize(app: sanic.app, loop):
    redis_connection_info = (
        app.redis_connection_info
        if hasattr(app, "redis_connection_info")
        else settings.redis_connection_info
    )

    await RedisConnection.initialize(redis_connection_info)
