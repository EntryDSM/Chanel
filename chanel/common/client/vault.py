from typing import Dict

from hvac import Client
from hvac.exceptions import InvalidRequest

from sanic.log import logger

from chanel.common.constant import GITHUB_TOKEN, RUN_ENV, VAULT_ADDRESS, SERVICE_NAME


class VaultClient:
    _redis_credential: Dict = None
    vault_client: Client = None

    @classmethod
    def initialize(cls):

        if GITHUB_TOKEN and not cls.vault_client:
            cls.vault_client = Client(VAULT_ADDRESS)
            cls.vault_client.auth.github.login(token=GITHUB_TOKEN)

            logger.info("Vault: initialized") \
                if cls.vault_client.is_authenticated() \
                else logger.error("Vault: not authenticated")

        else:
            logger.error("Vault: failed to initialize")

    @classmethod
    def __getattr__(cls, item: str):
        if not cls.vault_client:
            cls.initialize()

        try:
            return cls.vault_client.read(f"/service-secret/{RUN_ENV}/{SERVICE_NAME}")["data"][item]

        except InvalidRequest as e:
            logger.error("Vault: missing client token")
            raise e

        except KeyError as e:
            logger.error(f"Vault: keyword {item} doesn't exist")
            raise e

        except TypeError as e:
            logger.error(f"Vault: check the path")
            raise e

        except Exception as e:
            raise e

    @property
    def jwt_secret_key(self):
        return self.vault_client.read(f"/service-secret/{RUN_ENV}/jwt-key")["data"]["key"]

    @property
    def jwt_access_expire(self):
        return self.vault_client.read(f"/service-secret/{RUN_ENV}/jwt-key")["data"]["access_expire"]

    @property
    def jwt_refresh_expire(self):
        return self.vault_client.read(f"/service-secret/{RUN_ENV}/jwt-key")["data"]["refresh_expire"]

    @property
    def sendgrid_api_key(self):
        return self.vault_client.read(f"/secret/sendgrid")["data"]["API_KEY"]


class Setting:
    vault_client: VaultClient = None

    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item):
        return self.vault_client.__getattr__(item)

    @property
    def redis_connection_info(self):
        return {
            "address": f"redis://:{self.vault_client.REDIS_PASSWORD}@{self.vault_client.REDIS_HOST}:"
                       f"{self.vault_client.REDIS_PORT}",
            "minsize": 5,
            "maxsize": 10
        }

    @property
    def jwt_secret_key(self):
        return self.vault_client.jwt_secret_key

    @property
    def jwt_access_expire(self):
        return self.vault_client.jwt_access_expire

    @property
    def jwt_refresh_expire(self):
        return self.vault_client.jwt_refresh_expire

    @property
    def sendgrid_api_key(self):
        return self.vault_client.sendgrid_api_key

    DEBUG = False if RUN_ENV == "prod" else True


settings = Setting(VaultClient())
