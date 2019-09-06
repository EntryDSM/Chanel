from sanic.response import HTTPResponse, json

from chanel.applicant.domain.temp_applicant import TempApplicant, TempApplicantCacheRepository
from chanel.common import BadRequest
from chanel.common.constant import VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT
from chanel.common.exception import Conflict, Forbidden, InvalidSyntaxException
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.mail import email_checker, send_email


class SignUpService:
    external_repo: ExternalServiceRepository = None
    cache_repo: TempApplicantCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None,
                 cache_repo: TempApplicantCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def send_verify_email(self, temp_applicant: TempApplicant, resend: bool) -> HTTPResponse:
        try:
            email_checker(temp_applicant.email)

        except InvalidSyntaxException as e:
            raise BadRequest(e)

        already_exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(temp_applicant.email)
        already_exists_on_cache = await self.cache_repo.get_by_email(temp_applicant.email)

        if already_exists_on_hermes:
            raise Conflict("user already exists.")

        if already_exists_on_cache:
            if not resend:
                raise Forbidden("please try again later.")

            await self.cache_repo.delete(temp_applicant)

        await self.cache_repo.save(temp_applicant.generate_verify_code())

        send_email(temp_applicant.email, VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT.format(temp_applicant.verify_code))
        return json(dict(msg="sent a email successful."))
