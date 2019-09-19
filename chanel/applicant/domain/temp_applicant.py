from dataclasses import dataclass
from secrets import token_urlsafe
from typing import Type

from chanel.common.client.redis import RedisConnection
from chanel.common.domain.entity import BaseEntityClass
from chanel.common.exception import NotFoundFromCache


@dataclass
class TempApplicant(BaseEntityClass):
    email: str
    verify_code: str

    def __init__(self, email: str, verify_code: str = None):
        self.email = email

        if not verify_code:
            verify_code = self.generate_verify_code()

        self.verify_code = verify_code

    @property
    def key(self) -> str:
        return f"chanel:temp_applicant:verify:{self.email}"

    @property
    def value(self) -> str:
        return f"chanel:temp_applicant:verify:{self.verify_code}"

    def generate_verify_code(self):
        self.verify_code = token_urlsafe(4)
        return self

    @classmethod
    def data_to_entity(cls, email, verify_code=None):
        if type(email) == bytes:
            email = email.split(b':')[3].decode()

        if type(verify_code) == bytes:
            verify_code = verify_code.split(b':')[3].decode()

        if not verify_code:
            verify_code = token_urlsafe(4)

        return TempApplicant(email, verify_code)


class TempApplicantCacheRepository:
    def __init__(self, client: Type[RedisConnection]):
        self.client = client

    async def save(self, temp_applicant: TempApplicant, expire: int = None) -> None:
        await self.client.set(temp_applicant.key, temp_applicant.value, expire, pair=True)

    async def delete(self, temp_applicant: TempApplicant) -> None:
        await self.client.delete(temp_applicant.key, pair=True)

    async def get_by_email(self, email: str):
        refresh = await self.client.get(f"chanel:temp_applicant:verify:{email}")

        if not refresh:
            return None;

        return TempApplicant.data_to_entity(email, refresh)

    async def get_by_refresh(self, verify_code: str) -> TempApplicant:
        email = await self.client.get(f"chanel:applicant:verify:{verify_code}")

        if not email:
            raise NotFoundFromCache()

        return TempApplicant.data_to_entity(email, verify_code)
