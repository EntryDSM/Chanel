from abc import ABC, abstractmethod
from typing import Any, Dict


class PasswordResetVerificationRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        ...
