from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse, json

from chanel.common.client.http import HTTPClient
from chanel.common.client.redis import RedisConnection
from chanel.common import json_verify, query_parameter_verify, BadRequest
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.applicant.service.signup import SignUpService
from chanel.applicant.domain.temp_applicant import TempApplicant
from chanel.applicant.domain.temp_applicant import TempApplicantCacheRepository
from chanel.common.mail import check_email_syntax

signup_bp: Blueprint = Blueprint("applicant_signup")


class CreateApplicantAccount(HTTPMethodView):
    decorators = [json_verify(dict(email=str, password=str)), check_email_syntax()]

    service = SignUpService(
        ExternalServiceRepository(HTTPClient),
        TempApplicantCacheRepository(RedisConnection)
    )

    async def post(self, request: Request) -> HTTPResponse:
        email = request.json.get("email")
        password = request.json.get("password")

        response = await self.service.create_account(email, password)

        return response


class VerifyApplicantSignUpCode(HTTPMethodView):
    decorators = [
        query_parameter_verify(["code"]),
        check_email_syntax(email_url_index=8)
    ]

    service = SignUpService(
        ExternalServiceRepository(HTTPClient),
        TempApplicantCacheRepository(RedisConnection)
    )

    async def get(self, request: Request, email, verify_code) -> HTTPResponse:
        temp_applicant = TempApplicant(email, verify_code)
        response = await self.service.check_verify_code(temp_applicant)

        return response


class VerifyApplicantEmail(HTTPMethodView):
    decorators = [json_verify({"email": str}), check_email_syntax()]

    service = SignUpService(
        ExternalServiceRepository(HTTPClient),
        TempApplicantCacheRepository(RedisConnection)
    )

    async def post(self, request: Request) -> HTTPResponse:
        resend = True if request.args.get("resend") else False

        temp_applicant = TempApplicant(request.json.get("email")).generate_verify_code()
        response = await self.service.send_verify_email(temp_applicant, resend)

        return response


signup_bp.add_route(CreateApplicantAccount.as_view(), "/signup")
signup_bp.add_route(VerifyApplicantSignUpCode.as_view(), "/signup/verify/<email>/<verify_code>")
signup_bp.add_route(VerifyApplicantEmail.as_view(), "/signup/verify")
