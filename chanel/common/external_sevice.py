from ujson import loads

from chanel.applicant.domain.applicant import Applicant
from chanel.common.client.http import HTTPClient
from chanel.common.constant import GET_ADMIN_AUTH, ONE_ADMIN, GET_APPLICANT_AUTH, ONE_APPLICANT
from chanel.common.exception import BadRequest, Unauthorized, Forbidden, NotFound


class ExternalServiceRepository:
    client: HTTPClient = None

    def __init__(self, client):
        self.client = client

    async def get_admin_auth_from_hermes(self, admin_id: str, password: str) -> bool:
        response = await self.client.post(url=GET_ADMIN_AUTH.format(admin_id), json={"password": password})

        if response["status"] == 200:
            return True

        elif response["status"] == 400:
            raise BadRequest("bad request from inter-service")

        elif response["status"] == 403:
            raise Forbidden("authorization failed from inter-service")

    async def get_admin_info_from_hermes(self, admin_id: str):
        response = await self.client.get(url=ONE_ADMIN.format(admin_id))

        if response["status"] == 200:
            return response["data"]

        elif response["status"] == 401:
            raise Unauthorized("authentication failed from inter-service")

        elif response["status"] == 404:
            raise NotFound("admin not found from inter-service")

    async def get_applicant_auth_from_hermes(self, email: str, password: str) -> bool:
        response = await self.client.post(url=GET_APPLICANT_AUTH.format(email), json={"password": password})

        if response["status"] == 200:
            return True

        elif response["status"] == 400:
            raise BadRequest("bad request from inter-service")

        elif response["status"] == 403:
            raise Forbidden("authorization failed from inter-service")

    async def get_applicant_info_from_hermes(self, email: str):
        response = await self.client.get(url=ONE_APPLICANT.format(email))

        if response["status"] == 200:
            return loads(response["data"])

        elif response["status"] == 401:
            raise Unauthorized("authentication failed from inter-service")

        elif response["status"] == 404:
            return None
