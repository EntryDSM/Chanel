from sanic import Blueprint
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse, json

from chanel.common.client.http import HTTPClient
from chanel.common.client.redis import RedisConnection
from chanel.common import json_verify, query_parameter_verify
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.applicant.service.signup import SignUpService
from chanel.applicant.domain.temp_applicant import TempApplicant
from chanel.applicant.domain.temp_applicant import TempApplicantCacheRepository

signup_bp: Blueprint = Blueprint("applicant_signup")


class CreateApplicantTempAccount(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        return json(dict(msg="say hello"), 200)


class VerifyApplicantSignUpCode(HTTPMethodView):
    decorators = [query_parameter_verify(["code"])]

    async def get(self, request: Request) -> HTTPResponse:
        return json(dict(msg="say hello"), 200)


class VerifyApplicantEmail(HTTPMethodView):
    decorators = [json_verify({"email": str})]

    service = SignUpService(
        ExternalServiceRepository(HTTPClient),
        TempApplicantCacheRepository(RedisConnection)
    )

    async def post(self, request: Request) -> HTTPResponse:
        resend = True if request.args.get("resend") else None

        temp_applicant = TempApplicant(request.json.get("email")).generate_verify_code()
        response = await self.service.send_verify_email(temp_applicant, resend)

        return response


signup_bp.add_route(CreateApplicantTempAccount.as_view(), "/signup")
signup_bp.add_route(VerifyApplicantSignUpCode.as_view(), "/signup/verify")
signup_bp.add_route(VerifyApplicantEmail.as_view(), "/signup/verify")
