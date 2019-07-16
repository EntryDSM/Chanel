from sanic.views import HTTPMethodView
from sanic.blueprints import Blueprint
from sanic.response import json
from secrets import token_urlsafe
from werkzeug.security import generate_password_hash
from aiohttp import ClientResponse

from chanel.mail import send_email
from chanel.exception import BadRequest, Unauthorized, NotFound
from chanel.redis import RedisConnection
from chanel.setting import PATCH_ONE_USER
from chanel.client import HTTPClient
from chanel.env_variable import SERVICE_NAME

password_bp = Blueprint("reset_password", url_prefix="/password")


class ResetUserPassword(HTTPMethodView):

    async def get(self, request):
        verify_code = request.args["verify"][0]
        verify_code_has_saved = await RedisConnection.get(str({"verify": verify_code}))
        if verify_code_has_saved:
            return json("", status=404)
        else:
            raise BadRequest

    async def post(self, request):
        email = request.args["email"][0]
        verify_code = token_urlsafe(6)
        await RedisConnection.set_pair(f"{SERVICE_NAME}:verify:{email}", str({"verify": verify_code}))
        # TODO Email form 적용하기
        send_email(
            to_email=email,
            title="[대덕소프트웨어마이스터고등학교 입학전형시스템] 비밀번호 변경을 위한 메일입니다.",
            content=verify_code
        )

    async def put(self, request):
        verify_code = request.args["verify"][0]
        set_password = generate_password_hash(request.json["password"])
        verify_code_has_saved = await RedisConnection.get(str({"verify": verify_code}))
        email = verify_code_has_saved.split(":")[2]
        if verify_code and set_password and verify_code_has_saved:
            change_info: ClientResponse = (
                await HTTPClient.patch(PATCH_ONE_USER.format(email), json={"password": set_password})
            )
            if change_info.status == 200:
                return json("", status=200)
            else:
                raise BadRequest
        elif not verify_code_has_saved:
            raise Unauthorized

password_bp.add_route(ResetUserPassword.as_view(), "/reset")
