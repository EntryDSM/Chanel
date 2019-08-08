from dataclasses import dataclass

import ujson

from chanel.common.entity import BaseEntityClass


@dataclass(init=True)
class TempApplicant(BaseEntityClass):
    email: str

    @property
    def key(self) -> str:
        return f"chanel:temp_applicant:{self.email}"

    @property
    def value(self) -> str:
        return ujson.dumps(self.__dict__)
