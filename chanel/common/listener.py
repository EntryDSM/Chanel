from sanic.log import logger
from sanic import Sanic

from chanel.common.client.redis import RedisClient
from chanel.common.client.vault import settings


async def initialize(app: Sanic, loop):
    await RedisClient.initialize(settings.redis_connection_info)

    logger.info("successfully initialized redis client")


async def finalize(app: Sanic, loop):
    await RedisClient.destroy()

    logger.info("successfully finalized redis client")
