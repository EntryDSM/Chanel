from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

signup_bp: Blueprint = Blueprint("applicant_signup")


class CreateApplicantTempAccount(HTTPMethodView):

    def post(self, request: Request) -> HTTPResponse:
        ...


class VerifyApplicantEmail(HTTPMethodView):
    def get(self, request: Request) -> HTTPResponse:
        ...

    def post(self, request: Request) -> HTTPResponse:
        ...


signup_bp.add_route(CreateApplicantTempAccount.as_view(), "/signup")
signup_bp.add_route(VerifyApplicantEmail.as_view(), "/signup/verify")
