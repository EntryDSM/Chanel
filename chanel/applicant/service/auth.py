from sanic.response import json
from sanic_jwt_extended import create_refresh_token, create_access_token

from chanel.applicant.domain.applicant import Applicant, ApplicantCacheRepository
from chanel.common.constant import APPLICANT
from chanel.common.exception import Forbidden, BadRequest
from chanel.common.external_sevice import ExternalServiceRepository


class ApplicantService:
    external_repo: ExternalServiceRepository = None
    cache_repo: ApplicantCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None, cache_repo: ApplicantCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def login(self, request):
        email = request.json.get("email")
        password = request.json.get("password")

        authorized = await self.external_repo.get_applicant_auth_from_hermes(email, password)

        if authorized:
            saved_refresh = await self.cache_repo.get_by_email(email)
            if saved_refresh:
                await self.cache_repo.delete(saved_refresh)

            access = await create_access_token(identity=email, role=APPLICANT, app=request.app)
            refresh = await create_refresh_token(identity=email, app=request.app)

            await self.cache_repo.save(
                Applicant(email, refresh), int(request.app.config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds())
            )

            return json(dict(msg="login success", access=access, refresh=refresh), 201)

        else:
            raise Forbidden("Can not find match applicant info")

    async def refresh(self, request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise BadRequest("missing 'Bearer '")

        saved = await self.cache_repo.get_by_refresh(refresh)
        print(saved)

        if saved and refresh == saved.refresh_token:
            access = await create_access_token(identity=saved.email, role=APPLICANT, app=request.app)
            return json(dict(msg="refresh succeed", access=access), 201)

        else:
            raise Forbidden("incorrect refresh token")

    async def logout(self, request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise BadRequest("missing 'Bearer '")

        saved = await self.cache_repo.get_by_refresh(refresh)

        if not saved or refresh is not saved.refresh_token:
            raise Forbidden("incorrect refresh token")

        await self.cache_repo.delete(saved)

        return json(dict(msg="logout succeed"), 202)
