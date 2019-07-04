from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView


class CreateUserToken(HTTPMethodView):
    async def post(self, request):
        user_info = request.json['email']
        password = request.json['password']


class RefreshUserToken(HTTPMethodView):
    async def patch(self, request):
        pass


class DeleteUserToken(HTTPMethodView):
    async def delete(self, request):
        pass


class CreateAdminToken(HTTPMethodView):
    async def post(self, request):
        pass


class RefreshAdminToken(HTTPMethodView):
    async def patch(self, request):
        pass


class DeleteAdminToken(HTTPMethodView):
    async def delete(self, request):
        pass
