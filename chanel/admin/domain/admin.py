from dataclasses import dataclass

import ujson

from chanel.common.entity import BaseEntityClass


@dataclass
class Admin(BaseEntityClass):
    admin_id: str
    refresh_token: str

    @property
    def key(self) -> str:
        return f"chanel:admin:{self.admin_id}"

    @property
    def value(self) -> str:
        return ujson.dumps(self.__dict__)
