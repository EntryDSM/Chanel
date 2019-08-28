from dataclasses import dataclass

import ujson

from chanel.common.domain.entity import BaseEntityClass


@dataclass
class TempApplicant(BaseEntityClass):
    email: str

    @property
    def key(self) -> str:
        return f"chanel:temp_applicant:{self.email}"

    @property
    def value(self) -> str:
        return ujson.dumps(self.__dict__)
