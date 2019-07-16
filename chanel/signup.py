from aiohttp import ClientResponse
from secrets import token_urlsafe
from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json, HTTPResponse
from werkzeug.security import generate_password_hash, check_password_hash

from chanel.client import HTTPClient
from chanel.exception import Conflict, BadRequest, Unauthorized
from chanel.redis import RedisConnection
from chanel.setting import GET_ONE_APPLICANT, CREATE_NEW_APPLICANT
from chanel.env_variable import SERVICE_NAME

signup_bp = Blueprint("signup", url_prefix="/signup")


class SignUp(HTTPMethodView):
    async def post(self, request) -> HTTPResponse:
        email = request.json["email"]
        password = request.json["password"]
        check_account_conflict: ClientResponse = await HTTPClient.get(url=GET_ONE_APPLICANT.format(email))
        if email and password and check_account_conflict.status == 404:
            secured_password = generate_password_hash(password)
            await RedisConnection.set_pair(
                key=f"{SERVICE_NAME}:temp:{token_urlsafe(16)}",
                value=str({"email": email, "password": secured_password})
            )
            return json({"status": "temporary user has created."}, 202)
        elif check_account_conflict.status == 200:
            raise Conflict
        else:
            raise BadRequest


class SignUpVerify(HTTPMethodView):
    async def get(self, request) -> HTTPResponse:
        code = request.args['code'][0]
        temp_user = await RedisConnection.get(code)
        if temp_user:
            user_info = {
                "email": temp_user.email,
                "password": temp_user.password,
            }
            create_user = await HTTPClient.post(url=CREATE_NEW_APPLICANT, json=user_info)
            if create_user.status == 201:
                await RedisConnection.delete_pair(f"{SERVICE_NAME}:temp:{code}")
                return json("", status=200)
            else:
                raise Unauthorized
        else:
            raise Unauthorized


signup_bp.add_route(SignUp.as_view(), "/")
signup_bp.add_route(SignUpVerify.as_view(), "/verify")
