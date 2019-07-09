from chanel.config.vault import VaultClient


class Setting:
    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item, pwd=None):
        return self.vault_client.__getattr__(item) if not pwd else self.vault_client.__getattr__(item, pwd)

    @property
    def redis_connection_info(self):
        return {
            "address": (f"redis://:{self.vault_client.REDIS_PASSWORD}"
                        f"@{self.vault_client.REDIS_HOST}:{self.vault_client.REDIS_PORT}"),
            "minsize": 5,
            "maxsize": 10,
        }


settings = Setting(VaultClient())
