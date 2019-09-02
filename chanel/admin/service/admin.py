from sanic.response import json
from sanic_jwt_extended import create_refresh_token, create_access_token

from chanel.admin.domain.admin import AdminCacheRepository, Admin
from chanel.common.exception import Forbidden, BadRequest
from chanel.common.external_sevice import ExternalServiceRepository


class AdminService:
    external_repo: ExternalServiceRepository = None
    cache_repo: AdminCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None, cache_repo: AdminCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def login(self, request):
        admin_id = request.json.get("admin_id")
        password = request.json.get("password")

        authorized = await self.external_repo.get_admin_auth_from_hermes(admin_id, password)
        admin_info = await self.external_repo.get_admin_info_from_hermes(admin_id) if authorized else None

        if authorized and admin_info:
            saved_refresh = await self.cache_repo.get_by_id(admin_id)
            if saved_refresh:
                await self.cache_repo.delete(saved_refresh)

            access = await create_access_token(identity=admin_id, role=admin_info["admin_type"], app=request.app)
            refresh = await create_refresh_token(identity=admin_id, app=request.app)

            await self.cache_repo.save(
                Admin(admin_id, refresh), int(request.app.config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds())
            )

            return json(dict(msg="login success", access=access, refresh=refresh), 201)

        else:
            raise Forbidden("can't find match admin info")

    async def refresh(self, request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise BadRequest("missing 'Bearer '")

        saved = await self.cache_repo.get_by_refresh(refresh)

        admin_info = await self.external_repo.get_admin_info_from_hermes(saved.admin_id) if saved else None
        role = admin_info["admin_type"] if admin_info else None

        if saved and role and refresh == saved.refresh_token:
            access = await create_access_token(identity=saved.admin_id, role=role, app=request.app)
            return json(dict(msg="refresh succeed", access=access), 201)

        else:
            raise Forbidden("incorrect refresh token")

    async def logout(self, request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise BadRequest("missing 'Bearer '")

        saved = await self.cache_repo.get_by_refresh(refresh)

        if saved and refresh == saved.refresh_token:
            await self.cache_repo.delete(saved)
            return json(dict(msg="logout succeed"), 202)

        else:
            raise Forbidden("incorrect refresh token")
