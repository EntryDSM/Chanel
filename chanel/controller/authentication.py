import uuid

from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic.blueprints import Blueprint
from sanic_jwt_extended import jwt_required, create_access_token, create_refresh_token

from chanel.exceptions.http import Forbidden
from chanel.config import SERVICE_NAME
from chanel.config.setting import SETTINGS
from chanel.service.authentication import ApplicantAuthenticationService
from chanel.repository.account import ApplicantEmailVerificationRepository
from chanel.repository.authentication import ApplicantAuthenticationRepository, AdminAuthenticationRepository
from chanel.repository.connections import RedisConnection
from chanel.repository.password import PasswordResetVerificationRepository

user_auth_bp = Blueprint("user_auth")
admin_auth_bp = Blueprint("admin_auth", url_prefix="/admin")


class ApplicantAuthenticationView(HTTPMethodView):
    repository = ApplicantAuthenticationRepository(SETTINGS.hermes_host)
    service = ApplicantAuthenticationService(repository)


class CreateUserToken(ApplicantAuthenticationView):

    async def post(self, request) -> HTTPResponse:
        email = request.json['email']
        password = request.json['password']
        response = await self.service.create_token(request, email, password)
        return response


class RefreshUserToken(ApplicantAuthenticationView):
    async def patch(self, request):
        refresh = request.headers["X-Refresh-Token"]


class DeleteUserToken(ApplicantAuthenticationView):
    async def delete(self, request):
        ...


class CreateAdminToken(HTTPMethodView):
    async def post(self, request):
        ...


class RefreshAdminToken(HTTPMethodView):
    async def patch(self, request):
        ...


class DeleteAdminToken(HTTPMethodView):
    async def delete(self, request):
        ...


user_auth_bp.add_route(CreateUserToken.as_view(), "/login")
user_auth_bp.add_route(RefreshUserToken.as_view(), "/refresh")
user_auth_bp.add_route(DeleteUserToken.as_view(), "/logout")
admin_auth_bp.add_route(CreateAdminToken.as_view(), "/login")
admin_auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
admin_auth_bp.add_route(DeleteAdminToken.as_view(), "/logout")
