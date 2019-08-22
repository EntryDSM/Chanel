from sanic import app
from sanic.log import logger

from chanel.common.client.redis import RedisConnection
from chanel.common.client.vault import settings


async def initialize(app: app, loop):
    await RedisConnection.initialize(settings.redis_connection_info)
    logger.info("successfully initialized redis client")


async def finalize(app: app, loop):
    await RedisConnection.destroy()

    logger.info("successfully finalized redis client")
