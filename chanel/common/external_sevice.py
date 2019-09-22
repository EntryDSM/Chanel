from aiohttp import ClientResponseError

from chanel.common.client.http import HTTPClient
from chanel.common.constant import GET_ADMIN_AUTH, ONE_ADMIN, GET_APPLICANT_AUTH, ONE_APPLICANT, CREATE_NEW_APPLICANT
from chanel.common.exception import BadRequestFromInterService, ForbiddenFromInterService, Conflict, \
    NotFoundFromInterService


class ExternalServiceRepository:
    client: HTTPClient = None

    def __init__(self, client):
        self.client = client

    async def get_admin_auth_from_hermes(self, admin_id: str, password: str) -> bool:
        try:
            await self.client.post(url=GET_ADMIN_AUTH.format(admin_id), json={"password": password})
            return True

        except ClientResponseError as e:
            if e.status == 400:
                raise BadRequestFromInterService()

            elif e.status == 403:
                raise ForbiddenFromInterService()

            else:
                raise

    async def get_admin_info_from_hermes(self, admin_id: str):
        try:
            response = await self.client.get(url=ONE_ADMIN.format(admin_id))
            return response["data"]

        except ClientResponseError as e:
            if e.status == 404:
                return None

            else:
                raise

    async def get_applicant_auth_from_hermes(self, email: str, password: str) -> bool:
        try:
            await self.client.post(url=GET_APPLICANT_AUTH.format(email), json={"password": password})
            return True

        except ClientResponseError as e:
            if e.status == 400:
                raise BadRequestFromInterService()

            elif e.status == 403:
                raise ForbiddenFromInterService()

            elif e.status == 404:
                raise NotFoundFromInterService()

            else:
                raise

    async def get_applicant_info_from_hermes(self, email: str):
        try:
            response = await self.client.get(url=ONE_APPLICANT.format(email))
            return response["data"]

        except ClientResponseError as e:
            if e.status == 404:
                return None

            else:
                raise

    async def patch_one_applicant(self, email: str, data: dict):
        try:
            response = await self.client.patch(url=ONE_APPLICANT.format(email), json=data)
            return response["data"]

        except ClientResponseError as e:
            if e.status == 400:
                return None

            else:
                raise

    async def create_new_applicant(self, email, password) -> bool:
        try:
            await self.client.post(url=CREATE_NEW_APPLICANT, json={"email": email, "password": password})

        except ClientResponseError as e:
            if e.status == 409:
                raise Conflict("Applicant already exists.")

            else:
                raise

        return True
