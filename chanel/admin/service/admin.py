from datetime import timedelta
from sanic.response import json
from sanic_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash

from chanel.admin.domain.admin import AdminCacheRepository
from chanel.common.exception import Forbidden, BadRequest
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.client.vault import settings


class AdminService:
    external_repo: ExternalServiceRepository = None
    cache_repo: AdminCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None, cache_repo: AdminCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def login(self, request):
        admin_id = request.json.get("admin_id")
        password = generate_password_hash(request.json.get("password"))

        authorized = await self.external_repo.get_admin_auth_from_gateway(admin_id, password)

        if authorized:
            access = await create_access_token(identity=admin_id, role="ADMIN", app=request.app)
            refresh = await create_refresh_token(
                identity=admin_id,
                expires_delta=timedelta(days=settings.jwt_refresh_expire),
                app=request.app
            )

            return json(dict(msg="login success", access=access, refresh=refresh), 201)

        else:
            raise Forbidden("can't find match admin info")

    async def refresh(self, request):
        refresh = request.headers.get("X-Refresh-Token")
        saved = await self.cache_repo.get_by_refresh(refresh=refresh.split("Bearer ")[1])
        admin_info = await self.external_repo.get_admin_info_from_gateway(saved.key) if saved else None
        role = admin_info["admin_type"] if admin_info else None

        if refresh is saved and role:
            access = await create_access_token(identity=saved.key, role=role, app=request.app)
            return json(dict(msg="refresh success", access=access), 201)

        else:
            raise Forbidden("incorrect refresh token")

    async def logout(self, request):
        refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        saved = await self.cache_repo.get_by_refresh(refresh)

        if refresh is saved:
            await self.cache_repo.delete(saved)
            return json(dict(msg="logout success"), 202)

        else:
            raise Forbidden("incorrect refresh token")
