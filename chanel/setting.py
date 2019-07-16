from sanic import app
from sanic.log import logger

from chanel.env_variable import RUN_ENV
from chanel.redis import RedisConnection
from chanel.vault import VaultClient

SENDGRID_API_KEY = getattr(VaultClient, "/secret/sendgrid", "API_KEY")

LOGO = """
   ___  _                          _ 
  / __\| |__    __ _  _ __    ___ | |
 / /   | '_ \  / _` || '_ \  / _ \| |
/ /___ | | | || (_| || | | ||  __/| |
\____/ |_| |_| \__,_||_| |_| \___||_|
"""


class SETTINGS:
    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item):
        return self.vault_client.__getattr__(item)

    @property
    def redis_connection_info(self):
        return {
            "address": f"redis://:{self.vault_client.REDIS_PASSWORD}"
            f"@{self.vault_client.REDIS_HOST}:{self.vault_client.REDIS_PORT}",
            "minsize": 5,
            "maxsize": 10,
        }

    @property
    def hermes_host(self):
        return "hermes"

    @property
    def jwt_secret_key(self):
        return self.vault_client.client.read("/service-secret/prod/jwt-key")["data"]["key"]

    DEBUG = (False if RUN_ENV == "prod" else True)


SETTINGS = SETTINGS(VaultClient())
HERMES = SETTINGS.hermes_host
GET_ONE_APPLICANT = HERMES + "/applicant/{0}"
GET_ONE_ADMIN = HERMES + "/admin/{0}"
CREATE_NEW_APPLICANT = HERMES + "/applicant"
GET_USER_AUTH = HERMES + "/applicant/{0}/authorization"
GET_ADMIN_AUTH = HERMES + "/admin/{0}/authorization"
PATCH_ONE_USER = HERMES + "/applicant/{0}"


async def initialize(app: app, loop):
    redis_connection_info = (
        app.redis_connection_info
        if hasattr(app, "redis_connection_info")
        else SETTINGS.redis_connection_info
    )

    await RedisConnection.initialize(redis_connection_info)

    logger.info("Connection initialize complete")
