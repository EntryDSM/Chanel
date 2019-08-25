from ujson import dumps, loads

from chanel.common.client.http import HTTPClient
from chanel.common.constant import GET_ADMIN_AUTH, ONE_ADMIN
from chanel.common.exception import BadRequest, Unauthorized, Forbidden, NotFound


class ExternalServiceRepository:
    client: HTTPClient = None

    def __init__(self, client):
        self.client = client

    async def get_admin_auth_from_gateway(self, admin_id: str, password: str) -> bool:
        response = await self.client.post(url=GET_ADMIN_AUTH.format(admin_id), json=dumps(dict(password=password)))

        if response["status"] == 200:
            return True

        elif response["status"] == 400:
            raise BadRequest("bad request from gateway")

        elif response["status"] == 403:
            raise Forbidden("authorization failed from gateway")

    async def get_admin_info_from_gateway(self, admin_id: str):
        response = await self.client.get(url=ONE_ADMIN.format(admin_id), )

        if response["status"] == 200:
            return loads(response["data"])

        elif response["status"] == 401:
            raise Unauthorized("authentication failed from gateway")

        elif response["status"] == 404:
            raise NotFound("admin not found from gateway")
