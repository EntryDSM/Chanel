from typing import Dict
from hvac import Client
from aioredis import create_pool

from chanel.config import (VAULT_ADDRESS, VAULT_TOKEN, RUN_ENV, GITHUB_TOKEN, SERVICE_NAME)


class VaultClient:
    _redis_credential = None

    @classmethod
    def initialize(cls):
        cls.client = Client(url=VAULT_ADDRESS)

        if VAULT_TOKEN:
            cls.client.token = VAULT_TOKEN
        elif GITHUB_TOKEN:
            cls.client.auth.github.login(token=GITHUB_TOKEN)

    def __getattr__(self, item):
        try:
            return self.client.read(f"service-secret/{RUN_ENV}/{SERVICE_NAME}")["data"][item]
        except KeyError as e:
            raise Exception(f"{item} is can't be fetched")
        except Exception as e:
            raise e

    @property
    def redis_credential(self):
        pass

    @staticmethod
    def create_redis_connection_pool():
        pool = await create_pool(
            f"""redis://{getattr(VaultClient, "REDIS_HOST")}""",
            password=str(getattr(VaultClient, "REDIS_PASSWORD")),
            encoding="UTF-8"
        )
        # TODO Completing the Redis connection pool

