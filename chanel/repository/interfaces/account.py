from abc import ABC, abstractmethod
from typing import Dict, Any


class ApplicantEmailVerificationRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        ...
