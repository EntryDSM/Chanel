from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

password_bp: Blueprint = Blueprint("applicant_password", url_prefix="/password")


class ResetApplicantPassword(HTTPMethodView):
    def get(self, request: Request) -> HTTPResponse:
        ...

    def post(self, request: Request) -> HTTPResponse:
        ...

    def put(self, request: Request) -> HTTPResponse:
        ...


password_bp.add_route(ResetApplicantPassword.as_view(), "/reset")
