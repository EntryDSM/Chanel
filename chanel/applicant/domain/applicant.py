from dataclasses import dataclass

import ujson

from chanel.common.entity import BaseEntityClass


@dataclass
class Applicant(BaseEntityClass):
    email: str
    refresh_token: str

    @property
    def key(self) -> str:
        return f"chanel:applicant:{self.email}"

    @property
    def value(self) -> str:
        return ujson.dumps(self.__dict__)
