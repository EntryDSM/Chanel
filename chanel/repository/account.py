from typing import Dict, Any, Type

from chanel.repository.interfaces.account import ApplicantEmailVerificationRepositoryInterface
from chanel.service.http import HTTPClient

GET_ONE_APPLICANT_API_URL = '/applicant/{0}'


class ApplicantEmailVerificationRepository(ApplicantEmailVerificationRepositoryInterface):
    def __init__(self, host: str, client: Type[HTTPClient] = HTTPClient):
        self.host: str = host + GET_ONE_APPLICANT_API_URL
        self.client = client

    async def get_one(self, email: str) -> Dict[str, Any]:
        return await self.client.get(self.host.format(email))
