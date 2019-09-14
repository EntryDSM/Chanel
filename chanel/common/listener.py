from sanic.log import logger

from chanel.common.client.redis import RedisConnection
from chanel.common.client.vault import settings
from chanel.common.client.http import HTTPClient


async def initialize(app, loop):
    redis_connection_info = (
        app.redis_connection_info
        if hasattr(app, "redis_connection_info")
        else settings.redis_connection_info
    )

    await RedisConnection.init(redis_connection_info)
    await HTTPClient.init()

    logger.info("successfully initialized redis client")


async def finalize(app, loop):
    await RedisConnection.destroy()
    logger.info("successfully finalized redis client")
