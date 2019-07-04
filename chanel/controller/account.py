from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from chanel.domain.user import TempUser
from chanel.exceptions.http import Conflict


class SignUp(HTTPMethodView):
    async def post(self, request):
        user = TempUser(request.json["email"], request.json["password"])
        if user.is_conflict_account():
            raise Conflict
        user.build()
        return json({"status": "temporary user has created."}, 202)


class SignUpVerify(HTTPMethodView):
    async def get(self, request):
        code = request.args['code'][0]
        print(code)
        return json({"code": code}, 200)
