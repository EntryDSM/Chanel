from hvac import Client

from chanel.env_variable import VAULT_ADDRESS, VAULT_TOKEN, GITHUB_TOKEN, RUN_ENV, SERVICE_NAME


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
        except KeyError as exception:
            raise Exception(f"{item} is can't be fetched")
        except Exception as exception:
            raise exception

    @property
    def redis_credential(self):
        try:
            if not self._redis_credential:
                data = self.client.read(f"service-secret/{RUN_ENV}/{SERVICE_NAME}")["data"]
                self._redis_credential = {
                    "username": data["username"],
                    "password": data["password"],
                }
        except Exception as exception:
            raise exception

        return self._redis_credential
