from sanic.views import HTTPMethodView
from sanic.blueprints import Blueprint

password_bp = Blueprint("reset_password", url_prefix="/password")


class ResetUserPassword(HTTPMethodView):
    async def post(self, request):
        pass

    async def patch(self, request):
        pass


password_bp.add_route(ResetUserPassword.as_view(), "/reset")
