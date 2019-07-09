from abc import ABC, abstractmethod
from typing import Any, Dict


class ApplicantAuthenticationRepositoryInterface(ABC):
    @abstractmethod
    async def post(self, email: str, password: str) -> None:
        ...


class AdminAuthenticationRepositoryInterface(ABC):
    @abstractmethod
    async def post(self, admin_id: str, password: str) -> None:
        ...
