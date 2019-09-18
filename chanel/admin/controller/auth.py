from sanic import Blueprint
from sanic.views import HTTPMethodView

from chanel.common.client.http import HTTPClient
from chanel.admin.service.admin import AdminService
from chanel.common import json_verify, header_verify
from chanel.common.client.redis import RedisConnection
from chanel.admin.domain.admin import AdminCacheRepository
from chanel.common.external_sevice import ExternalServiceRepository

auth_bp: Blueprint = Blueprint("admin_auth")


class CreateAdminToken(HTTPMethodView):
    decorators = [json_verify(dict(admin_id=str, password=str))]

    service = AdminService(
        ExternalServiceRepository(HTTPClient),
        AdminCacheRepository(RedisConnection)
    )

    async def post(self, request):
        response = await self.service.login(request)

        return response


class RefreshAdminToken(HTTPMethodView):
    decorators = [header_verify(["X-Refresh-Token"])]

    service = AdminService(
        ExternalServiceRepository(HTTPClient),
        AdminCacheRepository(RedisConnection)
    )

    async def patch(self, request):
        response = await self.service.refresh(request)

        return response


class DestroyAdminToken(HTTPMethodView):
    decorators = [header_verify(["X-Refresh-Token"])]

    service = AdminService(None, AdminCacheRepository(RedisConnection))

    async def delete(self, request):
        response = await self.service.logout(request)

        return response


auth_bp.add_route(CreateAdminToken.as_view(), "/login")
auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
auth_bp.add_route(DestroyAdminToken.as_view(), "/logout")
