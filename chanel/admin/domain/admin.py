from dataclasses import dataclass
from typing import Type

import ujson

from chanel.common.entity import BaseEntityClass
from common.client.redis import RedisConnection


@dataclass
class Admin(BaseEntityClass):
    admin_id: str
    refresh_token: str

    @property
    def key(self) -> str:
        return f"chanel:admin:{self.admin_id}"

    @property
    def value(self) -> str:
        return ujson.dumps(
            {"refresh": self.refresh_token}
        )


class AdminCacheRepository:

    def __init__(self, client: Type[RedisConnection]):
        self.client = client

    async def save(self, admin: Admin, expire: int = None) -> None:
        await self.client.set_pair(admin.key, admin.value, expire)

    async def delete(self, admin: Admin) -> None:
        await self.client.delete_pair(admin.key)

    async def get_by_id(self, admin_id: str) -> Admin:
        value = await self.client.get(f"chanel:admin:{admin_id}")

        return Admin(admin_id, value) if value else None

    async def get_by_refresh(self, refresh: str) -> Admin:
        key = ujson.dumps({"refresh": refresh})
        admin_id = str(await self.client.get(key)).split(":")[2]

        return Admin(admin_id, refresh) if admin_id else None
