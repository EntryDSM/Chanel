from sanic.response import HTTPResponse, json
from ujson import dumps

from chanel.applicant.domain.temp_applicant import TempApplicant, TempApplicantCacheRepository
from chanel.common import BadRequest
from chanel.common.client.redis import RedisConnection
from chanel.common.constant import VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT
from chanel.common.exception import Conflict, Forbidden, Unauthorized, NotFound
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.mail import send_email


class SignUpService:
    external_repo: ExternalServiceRepository = None
    cache_repo: TempApplicantCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None,
                 cache_repo: TempApplicantCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def create_account(self, email: str, password: str) -> HTTPResponse:
        cached = await RedisConnection.get(f"chanel:temp_applicant:verified:{email}")
        if not cached:
            raise NotFound("account was not found.")

        exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(email)
        if not exists_on_hermes:
            if await self.external_repo.create_new_applicant(email, password):
                await RedisConnection.delete(f"chanel:temp_applicant:verified:{email}")

                return json(dict(msg="create user succeed."))

        else:
            raise Conflict("user already exists.")

    async def check_verify_code(self, temp_applicant: TempApplicant) -> HTTPResponse:
        exists_on_cache = await self.cache_repo.get_by_email(temp_applicant.email)

        if not exists_on_cache:
            raise BadRequest("bad request.")

        if temp_applicant != exists_on_cache:
            raise Unauthorized("incorrect verification code.")

        else:
            await self.cache_repo.delete(temp_applicant)
            await RedisConnection.set(f"chanel:temp_applicant:verified:{temp_applicant.email}",
                                      dumps({"verified": True}))

            return json(dict(msg="verify user email succeed."), 200)

    async def send_verify_email(self, temp_applicant: TempApplicant, resend: bool) -> HTTPResponse:
        exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(temp_applicant.email)
        exists_on_cache = await self.cache_repo.get_by_email(temp_applicant.email)

        if exists_on_hermes:
            raise Conflict("user already exists.")

        if exists_on_cache:
            if not resend:
                raise Forbidden("please try again later.")

            await self.cache_repo.delete(temp_applicant)

        await self.cache_repo.save(temp_applicant.generate_verify_code(), expire=180)
        send_email(temp_applicant.email, VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT.format(temp_applicant.verify_code))

        return json(dict(msg="sent a email successful."))
