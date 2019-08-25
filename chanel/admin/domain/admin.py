from dataclasses import dataclass
from typing import Type

from common.client.redis import RedisConnection
from common.domain.entity import BaseEntityClass


@dataclass
class Admin(BaseEntityClass):
    admin_id: str
    refresh_token: str

    @property
    def key(self) -> str:
        return f"chanel:admin:refresh:{self.admin_id}"

    @property
    def value(self) -> str:
        return f"chanel:admin:refresh:{self.refresh_token}"

    @classmethod
    def data_to_entity(cls, admin_id: str, refresh_token: str):
        return Admin(
            admin_id.split(":")[3],
            refresh_token.split(":")[3]
        )


class AdminCacheRepository:
    def __init__(self, client: Type[RedisConnection]):
        self.client = client

    async def save(self, admin: Admin, expire: int = None) -> None:
        await self.client.set(admin.key, admin.value, expire, pair=True)

    async def delete(self, admin: Admin) -> None:
        await self.client.delete(admin.key, pair=True)

    async def get_by_id(self, admin_id: str) -> Admin:
        refresh = await self.client.get(f"chanel:admin:refresh:{admin_id}")

        return Admin.data_to_entity(admin_id, refresh) if refresh else None

    async def get_by_refresh(self, refresh: str) -> Admin:
        admin_id = await self.client.get(f"chanel:admin:refresh:{refresh}")

        return Admin.data_to_entity(admin_id, refresh) if admin_id else None
