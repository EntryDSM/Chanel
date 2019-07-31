from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView

auth_bp: Blueprint = Blueprint("applicant_auth")


class CreateApplicantToken(HTTPMethodView):
    def post(self, request: Request):
        ...


class RefreshApplicantToken(HTTPMethodView):
    def post(self, request: Request):
        ...


class DestroyApplicantToken(HTTPMethodView):
    def post(self, request: Request):
        ...


auth_bp.add_route(CreateApplicantToken.as_view(), "/login")
auth_bp.add_route(RefreshApplicantToken.as_view(), "/refresh")
auth_bp.add_route(DestroyApplicantToken.as_view(), "/logout")
