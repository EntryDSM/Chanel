from hvac import Client

from chanel.config import (VAULT_ADDRESS, VAULT_TOKEN, RUN_ENV, GITHUB_TOKEN)


class VaultClient:
    @classmethod
    def initialize(cls):
        cls.client = Client(url=VAULT_ADDRESS)

        if VAULT_TOKEN:
            cls.client.token = VAULT_TOKEN
        elif GITHUB_TOKEN:
            cls.client.auth.github.login(token=GITHUB_TOKEN)

