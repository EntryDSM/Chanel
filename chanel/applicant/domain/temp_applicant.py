from dataclasses import dataclass
from secrets import token_urlsafe
from typing import Type

from chanel.common.client.redis import RedisConnection
from chanel.common.domain.entity import BaseEntityClass


@dataclass
class TempApplicant(BaseEntityClass):
    email: str
    verify_code: str

    def __init__(self, email: str, verify_code):
        self.email = email
        self.verify_code = verify_code

    @property
    def key(self) -> str:
        return f"chanel:temp_applicant:verify:{self.email}"

    @property
    def value(self) -> str:
        return f"chanel:temp_applicant:verify{self.verify_token}"

    @classmethod
    def generate_verify_code(cls):
        cls.verify_code = token_urlsafe()

    @classmethod
    def data_to_entity(cls, email, verify_code):
        if type(email) == bytes:
            email = email.split(b':')[3].decode()

        if type(verify_code) == bytes:
            verify_code = verify_code.split(b':')[3].decode()

        return TempApplicant(email, verify_code)


class TempApplicantCacheRepository:
    def __init__(self, client: Type[RedisConnection]):
        self.client = client

    async def save(self, temp_applicant: TempApplicant, expire: int = None) -> None:
        await self.client.set(temp_applicant.key, temp_applicant.value, expire, pair=True)

    async def delete(self, temp_applicant: TempApplicant) -> None:
        await self.client.delete(temp_applicant.key, pair=True)

    async def get_by_email(self, email: str) -> TempApplicant:
        refresh = await self.client.get(f"chanel:temp_applicant:verify:{email}")

        return TempApplicant.data_to_entity(email, refresh) if refresh else None

    async def get_by_refresh(self, verify_code: str) -> TempApplicant:
        email = await self.client.get(f"chanel:applicant:verify:{verify_code}")

        return TempApplicant.data_to_entity(email, verify_code) if email else None
