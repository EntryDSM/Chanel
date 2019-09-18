from sanic import Blueprint
from sanic.views import HTTPMethodView

from chanel.common.client.http import HTTPClient
from chanel.common import json_verify, header_verify
from chanel.common.client.redis import RedisConnection
from chanel.applicant.service.auth import ApplicantService
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.applicant.domain.applicant import ApplicantCacheRepository

auth_bp: Blueprint = Blueprint("applicant_auth")


class CreateApplicantToken(HTTPMethodView):
    decorators = [json_verify(dict(email=str, password=str))]

    service = ApplicantService(
        ExternalServiceRepository(HTTPClient),
        ApplicantCacheRepository(RedisConnection)
    )

    async def post(self, request):
        response = await self.service.login(request)

        return response


class RefreshApplicantToken(HTTPMethodView):
    decorators = [header_verify(["X-Refresh-Token"])]

    service = ApplicantService(
        ExternalServiceRepository(HTTPClient),
        ApplicantCacheRepository(RedisConnection)
    )

    async def patch(self, request):
        response = await self.service.refresh(request)

        return response


class DestroyApplicantToken(HTTPMethodView):
    decorators = [header_verify(["X-Refresh-Token"])]

    service = ApplicantService(None, ApplicantCacheRepository(RedisConnection))

    async def delete(self, request):
        response = await self.service.logout(request)

        return response


auth_bp.add_route(CreateApplicantToken.as_view(), "/login")
auth_bp.add_route(RefreshApplicantToken.as_view(), "/refresh")
auth_bp.add_route(DestroyApplicantToken.as_view(), "/logout")
