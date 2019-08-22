import ujson
import sanic.response

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView

from admin.domain.admin import AdminCacheRepository, Admin
from common.client.redis import RedisConnection
from common.exception import Forbidden, BadRequest

auth_bp: Blueprint = Blueprint("admin_auth")


class CreateAdminToken(HTTPMethodView):
    repository: AdminCacheRepository = AdminCacheRepository

    async def post(self, request: Request):
        email = request.json.get("email")
        password = request.json.get("password")

        ...


class RefreshAdminToken(HTTPMethodView):
    repository: AdminCacheRepository = AdminCacheRepository

    async def post(self, request: Request):
        refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        saved_refresh = self.repository.get_by_refresh(refresh)

        ...


class DestroyAdminToken(HTTPMethodView):
    repository: AdminCacheRepository = AdminCacheRepository(RedisConnection)

    async def post(self, request: Request) -> HTTPResponse:
        refresh = str(request.headers.get("X-Refresh-Token")).split("Bearer ")[1]
        saved = await self.repository.get_by_refresh(refresh)

        if refresh and saved:
            await self.repository.delete(Admin(saved.key, saved.value))

            return json({"msg": "logout success"}, 202)

        elif not saved:
            raise Forbidden

        else:
            raise BadRequest


auth_bp.add_route(CreateAdminToken.as_view(), "/login")
auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
auth_bp.add_route(DestroyAdminToken.as_view(), "/logout")
