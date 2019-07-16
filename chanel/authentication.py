import uuid

from aiohttp import ClientResponse
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from chanel.setting import GET_USER_AUTH, GET_ADMIN_AUTH, GET_ONE_ADMIN
from chanel.exception import Forbidden, BadRequest
from chanel.client import HTTPClient
from chanel.redis import RedisConnection
from chanel.env_variable import SERVICE_NAME

SECONDS_FROM_30DAYS = 60 ** 2 * 24 * 30
user_auth_bp = Blueprint("user_auth")
admin_auth_bp = Blueprint("admin_auth", url_prefix="/admin")


class CreateUserToken(HTTPMethodView):
    async def post(self, request: Request) -> HTTPResponse:
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])
        user_auth_check = await HTTPClient.post(url=GET_USER_AUTH.format(email), json={"password": password})
        if user_auth_check.status == 200:
            access = create_access_token(app=request.app, identity=email, role="APPLICANT")
            refresh = str(uuid.uuid4())
            await RedisConnection.set_pair(
                key=f"{SERVICE_NAME}:user:{email}",
                value=str({"refresh": refresh}),
                expire=SECONDS_FROM_30DAYS
            )
            return json({"access": access, "refresh": refresh}, status=201)
        elif user_auth_check.status == 400:
            raise BadRequest
        elif user_auth_check.status == 403:
            raise Forbidden


class RefreshUserToken(HTTPMethodView):
    async def patch(self, request: Request) -> HTTPResponse:
        refresh = request.headers["X-Refresh-Token"]
        saved_refresh = await RedisConnection.get(refresh)
        if saved_refresh:
            access = create_access_token(app=request.app, identity=str(saved_refresh).split(":")[2], role="APPLICANT")
            return json({"access": access}, status=201)
        else:
            raise BadRequest


class DeleteUserToken(HTTPMethodView):
    async def delete(self, request: Request) -> HTTPResponse:
        refresh = request.headers["X-Refresh-Token"]
        saved_refresh = await RedisConnection.get(refresh)
        if refresh and saved_refresh:
            await RedisConnection.delete_pair(refresh)
            return json("", status=202)
        elif not refresh:
            raise BadRequest
        elif refresh and not saved_refresh:
            raise Forbidden


class CreateAdminToken(HTTPMethodView):
    async def post(self, request: Request):
        admin_id = request.json["admin_id"]
        password = generate_password_hash(request.json["password"])
        admin_auth_check = await HTTPClient.post(url=GET_ADMIN_AUTH.format(admin_id), json={"password": password})
        admin_info = await HTTPClient.get(url=GET_ONE_ADMIN.format(admin_id))
        if admin_auth_check.status == 200 and admin_info.status == 200:
            access = create_access_token(
                app=request.app,
                identity=admin_id,
                role=(await admin_info.json())["admin_type"],
            )
            refresh = str(uuid.uuid4())
            await RedisConnection.set_pair(
                key=f"""{SERVICE_NAME}:{(await admin_info.json())["admin_type"]}:{admin_id}""",
                value=str({"refresh": refresh}),
                expire=SECONDS_FROM_30DAYS
            )
            return json({"access": access, "refresh": refresh}, status=201)
        elif admin_auth_check.status == 400:
            raise BadRequest
        elif admin_auth_check.status == 403:
            raise Forbidden


class RefreshAdminToken(HTTPMethodView):
    async def patch(self, request: Request) -> HTTPResponse:
        refresh = request.headers["X-Refresh-Token"]
        saved_refresh: ClientResponse = await RedisConnection.get(refresh)
        admin_id = (await saved_refresh.json()).split(":")[2]
        admin_type = await HTTPClient.get(url=GET_ONE_ADMIN.format(admin_id))
        if saved_refresh:
            access = create_access_token(app=request.app, identity=admin_id, role=admin_type)
            return json({"access": access}, status=201)
        else:
            raise BadRequest


class DeleteAdminToken(HTTPMethodView):
    async def delete(self, request: Request) -> HTTPResponse:
        refresh = request.headers["X-Refresh-Token"]
        saved_refresh = await RedisConnection.get(refresh)
        if refresh and saved_refresh:
            await RedisConnection.delete_pair(refresh)
            return json("", status=202)
        elif not refresh:
            raise BadRequest
        elif not saved_refresh:
            raise Forbidden


user_auth_bp.add_route(CreateUserToken.as_view(), "/login")
user_auth_bp.add_route(RefreshUserToken.as_view(), "/refresh")
user_auth_bp.add_route(DeleteUserToken.as_view(), "/logout")
admin_auth_bp.add_route(CreateAdminToken.as_view(), "/login")
admin_auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
admin_auth_bp.add_route(DeleteAdminToken.as_view(), "/logout")
