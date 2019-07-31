from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView

auth_bp: Blueprint = Blueprint("admin_auth")


class CreateAdminToken(HTTPMethodView):
    def post(self, request: Request):
        ...


class RefreshAdminToken(HTTPMethodView):
    def post(self, request: Request):
        ...


class DestroyAdminToken(HTTPMethodView):
    def post(self, request: Request):
        ...


auth_bp.add_route(CreateAdminToken.as_view(), "/login")
auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
auth_bp.add_route(DestroyAdminToken.as_view(), "/logout")
