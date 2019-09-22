from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

from chanel.applicant.service.password import ChangePasswordService
from chanel.common import query_parameter_verify, json_verify
from chanel.common.client.http import HTTPClient
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.mail import check_email_syntax

password_bp: Blueprint = Blueprint("applicant_password", url_prefix="/password")


class SendPasswordResetVerificationEmail(HTTPMethodView):
    decorators = [query_parameter_verify(["email"]), check_email_syntax()]

    service = ChangePasswordService(
        ExternalServiceRepository(HTTPClient), None
    )

    def post(self, request: Request) -> HTTPResponse:
        email = request.json.get("email")

        response = await self.service.send_verify_email(email)

        return response


class CheckVerifyCodeExists(HTTPMethodView):
    decorators = [check_email_syntax(email_url_index=8)]

    service = ChangePasswordService(
        ExternalServiceRepository(HTTPClient), None
    )

    def get(self, request: Request, email: str, verify_code: str) -> HTTPResponse:
        response = await self.service.check_verify_code(email, verify_code)

        return response


class ResetApplicantPassword(HTTPMethodView):
    decorators = [json_verify({"email": str, "password": str})]

    service = ChangePasswordService(
        ExternalServiceRepository(HTTPClient), None
    )

    def put(self, request: Request) -> HTTPResponse:
        email = request.json.get("email")
        password = request.json.get("password")

        response = await self.service.reset_password(email, password)

        return response


password_bp.add_route(ResetApplicantPassword.as_view(), "/reset")
password_bp.add_route(CheckVerifyCodeExists.as_view(), "/reset/<email>/<verify_code>")
password_bp.add_route(ResetApplicantPassword.as_view(), "/reset")
