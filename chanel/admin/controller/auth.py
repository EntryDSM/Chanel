from sanic import Blueprint
from sanic.views import HTTPMethodView

from chanel.admin.domain.admin import AdminCacheRepository
from chanel.admin.service.admin import AdminService
from chanel.common import json_verify, header_verify
from chanel.common.client.http import HTTPClient
from chanel.common.client.redis import RedisConnection
from chanel.common.external_sevice import ExternalServiceRepository

auth_bp: Blueprint = Blueprint("admin_auth")


class CreateAdminToken(HTTPMethodView):
    decorators = [json_verify(dict(admin_id=str, password=str))]

    external_service_repository = ExternalServiceRepository(HTTPClient)
    service = AdminService(external_service_repository, None)

    async def post(self, request):
        response = await self.service.login(request)

        return response


class RefreshAdminToken(HTTPMethodView):
    decorators = [header_verify(["X-Refresh-Token"])]

    cache_repository: AdminCacheRepository = AdminCacheRepository(RedisConnection)
    external_service_repository = ExternalServiceRepository(HTTPClient)
    service = AdminService(external_service_repository, cache_repository)

    async def post(self, request):
        response = await self.service.refresh(request)

        return response


class DestroyAdminToken(HTTPMethodView):
    decorators = [header_verify(["X-Verify-Token"])]

    cache_repository: AdminCacheRepository = AdminCacheRepository(RedisConnection)
    service = AdminService(None, cache_repository)

    async def delete(self, request):
        response = await self.service.logout(request)

        return response


auth_bp.add_route(CreateAdminToken.as_view(), "/login")
auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
auth_bp.add_route(DestroyAdminToken.as_view(), "/logout")
