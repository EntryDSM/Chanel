from typing import Any, Dict, Type

from chanel.repository.interfaces.authentication import ApplicantAuthenticationRepositoryInterface, \
    AdminAuthenticationRepositoryInterface
from chanel.service.http import HTTPClient

GET_APPLICANT_AUTH_API_URL = '/applicant/{0}/authorization'
GET_ADMIN_AUTH_API_URL = '/admin/{0}/authorization'


class ApplicantAuthenticationRepository(ApplicantAuthenticationRepositoryInterface):
    def __init__(self, host: str, client: Type[HTTPClient] = HTTPClient):
        self.host: str = host + GET_APPLICANT_AUTH_API_URL
        self.client = client

    async def post(self, email: str, password: str) -> Dict[str, Any]:
        data = {"password": password}
        return await self.client.post(url=self.host.format(email), data=data)


class AdminAuthenticationRepository(AdminAuthenticationRepositoryInterface):
    def __init__(self, host: str, client: HTTPClient):
        self.host: str = host + GET_ADMIN_AUTH_API_URL
        self.client: HTTPClient = client

    async def post(self, admin_id: str, password: str) -> Dict[str, Any]:
        data = {"password": password}
        return await self.client.post(url=self.host.format(admin_id), data=data)
