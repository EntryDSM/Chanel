from dataclasses import dataclass
from typing import Type

from chanel.common.client.redis import RedisConnection
from chanel.common.domain.entity import BaseEntityClass


@dataclass
class Applicant(BaseEntityClass):
    email: str
    refresh_token: str

    @property
    def key(self) -> str:
        return f"chanel:applicant:refresh:{self.email}"

    @property
    def value(self) -> str:
        return f"chanel:applicant:refresh:{self.refresh_token}"

    @classmethod
    def data_to_entity(cls, email, refresh_token):
        if type(email) == bytes:
            email = email.split(b':')[3].decode()

        if type(refresh_token) == bytes:
            refresh_token = refresh_token.split(b':')[3].decode()

        return Applicant(email, refresh_token)


class ApplicantCacheRepository:
    def __init__(self, client: Type[RedisConnection]):
        self.client = client

    async def save(self, applicant: Applicant, expire: int = None) -> None:
        await self.client.set(applicant.key, applicant.value, expire, pair=True)

    async def delete(self, applicant: Applicant) -> None:
        await self.client.delete(applicant.key, pair=True)

    async def get_by_email(self, email: str) -> Applicant:
        refresh = await self.client.get(f"chanel:applicant:refresh:{email}")

        return Applicant.data_to_entity(email, refresh) if refresh else None

    async def get_by_refresh(self, refresh: str) -> Applicant:
        email = await self.client.get(f"chanel:applicant:refresh:{refresh}")

        return Applicant.data_to_entity(email, refresh) if email else None
