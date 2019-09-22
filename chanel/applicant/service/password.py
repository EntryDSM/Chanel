from secrets import token_urlsafe

from sanic.response import json
from ujson import dumps

from chanel.applicant.domain.applicant import ApplicantCacheRepository
from chanel.common.client.redis import RedisConnection
from chanel.common.exception import NotFound, Unauthorized
from chanel.common.external_sevice import ExternalServiceRepository
from chanel.common.mail import send_email
from chanel.common.constant import CHANGE_PASSWORD_EMAIL_TITLE, CHANGE_PASSWORD_EMAIL_CONTENT

BASE_VERIFY_KEY = "chanel:change_password:verify:{}"
BASE_VERIFIED_KEY = "chanel:change_password:verified:{}"


class ChangePasswordService:
    external_repo: ExternalServiceRepository = None

    def __init__(self, external_repo: ExternalServiceRepository = None,
                 cache_repo: ApplicantCacheRepository = None):
        self.external_repo = external_repo
        self.cache_repo = cache_repo

    async def send_verify_email(self, email: str):
        exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(email)
        exists_on_cache = await RedisConnection.get(BASE_VERIFY_KEY.format(email))

        if not exists_on_hermes:
            raise NotFound("user not found.")

        if exists_on_cache:
            await RedisConnection.delete(BASE_VERIFY_KEY.format(email), pair=True)

        verify_code = token_urlsafe(4)
        await RedisConnection.set(BASE_VERIFY_KEY.format(email), verify_code, pair=True)

        send_email(email, CHANGE_PASSWORD_EMAIL_TITLE, CHANGE_PASSWORD_EMAIL_CONTENT.format(verify_code))

        return json(dict(msg="sent a email successful."))

    async def check_verify_code(self, email: str, verify_code: str):
        exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(email)
        saved_code = await RedisConnection.get(BASE_VERIFY_KEY.format(email))

        if type(saved_code) is bytes:
            saved_code = saved_code.decode()

        if not exists_on_hermes or not saved_code or verify_code is not saved_code.decode():
            raise NotFound("user not found.")

        await RedisConnection.delete(saved_code, pair=True)
        await RedisConnection.set(BASE_VERIFIED_KEY.format(email), dumps({"verified": True}))

        return json(dict(msg="code has verified."))

    async def reset_password(self, email: str, password: str):
        exists_on_hermes = await self.external_repo.get_applicant_info_from_hermes(email)
        exists_on_cache = await RedisConnection.get(BASE_VERIFIED_KEY.format(email))

        if not exists_on_cache or not exists_on_hermes:
            raise Unauthorized("authentication failed.")

        await self.external_repo.patch_one_applicant(email, dict(password=password))

        return json(dict(msg="reset success."))
