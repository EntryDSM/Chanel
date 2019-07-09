from sanic.views import HTTPMethodView
from sanic.blueprints import Blueprint
from sanic_jwt_extended import jwt_required, create_access_token, create_refresh_token

user_auth_bp = Blueprint("user_auth")
admin_auth_bp = Blueprint("admin_auth", url_prefix="/admin")


class CreateUserToken(HTTPMethodView):
    async def post(self, request):
        user_info = request.json['email']
        password = request.json['password']
        if user_info and password and
            token = create_access_token(
                app=request.app, identity=user_info, user_claims=)


class RefreshUserToken(HTTPMethodView):
    async def patch(self, request):
        ...


class DeleteUserToken(HTTPMethodView):
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
