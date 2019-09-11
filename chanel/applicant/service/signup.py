from sanic.response import HTTPResponse, json
from werkzeug.security import generate_password_hash

from chanel.applicant.domain.temp_applicant import TempApplicant, TempApplicantCacheRepository
from chanel.common import BadRequest
from chanel.common.client.redis import RedisConnection
from chanel.common.constant import VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT
from chanel.common.exception import Conflict, Forbidden, Unauthorized, NotFound, NotFoundFromInterService, \
    NotFoundFromCache
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.mail import send_email


class SignUpService:
    external_repo: ExternalServiceRepository = None
    cache_repo: TempApplicantCacheRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None,
                 cache_repo: TempApplicantCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def send_verify_email(self, temp_applicant: TempApplicant, resend: bool) -> HTTPResponse:
        try:
            await self.external_repo.get_applicant_info_from_hermes(temp_applicant.email)

        except not NotFoundFromInterService:
            raise Conflict("user already exists.")

        try:
            await self.cache_repo.get_by_email(temp_applicant.email)

        except not NotFoundFromCache:
            if not resend:
                raise Forbidden("please try again later.")

            await self.cache_repo.delete(temp_applicant)

        await self.cache_repo.save(temp_applicant.generate_verify_code())
        send_email(temp_applicant.email, VERIFY_EMAIL_TITLE, VERIFY_EMAIL_CONTENT.format(temp_applicant.verify_code))

        return json(dict(msg="sent a email successful."))

    async def check_verify_code(self, temp_applicant: TempApplicant) -> HTTPResponse:
        try:
            already_exists_on_cache = await self.cache_repo.get_by_email(temp_applicant.email)

        except NotFoundFromCache:
            raise BadRequest("bad request.")

        if temp_applicant != already_exists_on_cache:
            raise Unauthorized("incorrect verification code.")

        else:
            await self.cache_repo.delete(temp_applicant)
            await RedisConnection.set(f"chanel:temp_applicant:verified:{temp_applicant.email}")

            return json(dict(msg="verify user email succeed."), 200)

    async def create_account(self, email: str, password: str) -> HTTPResponse:
        if not RedisConnection.get(f"chanel:temp_applicant:verified:{email}"):
            raise NotFound("account was not found.")

        elif await self.external_repo.get_applicant_info_from_hermes(email):
            raise Conflict("user already exists.")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256:50000")
        if await self.external_repo.create_new_applicant(email, hashed_password):
            return json(dict(msg="create user succeed."))
