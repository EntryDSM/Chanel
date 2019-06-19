from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView


class ResetUserPassword(HTTPMethodView):
    async def post(self, request):
        pass

    async def patch(self, request):
        pass
