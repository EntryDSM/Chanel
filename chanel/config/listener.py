import sanic

from sanic.log import logger

from chanel.config.setting import SETTINGS
from chanel.repository.connections import RedisConnection


async def initialize(app: sanic.app, loop):
    redis_connection_info = (
        app.redis_connection_info
        if hasattr(app, "redis_connection_info")
        else SETTINGS.redis_connection_info
    )

    hermes_host = (
        app.hermes_host
        if hasattr(app, "hermes_host")
        else SETTINGS.hermes_host
    )

    await RedisConnection.initialize(redis_connection_info)

    logger.info("Connection initialize complete")
