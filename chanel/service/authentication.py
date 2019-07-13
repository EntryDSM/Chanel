import uuid

from sanic.response import json
from sanic_jwt_extended import create_access_token, create_refresh_token

from chanel.config import SERVICE_NAME
from chanel.repository.authentication import ApplicantAuthenticationRepository
from chanel.repository.connections import RedisConnection
from chanel.exceptions.http import BadRequest, Forbidden

SECONDS_FROM_30DAYS = 60 ** 2 * 24 * 30

class ApplicantAuthenticationService:
    def __init__(self, repository: ApplicantAuthenticationRepository):
        self.repository = repository

    def create_token(self, request, email, password):
        user_auth = await self.repository.post(email, password)
        if user_auth.status == 201:
            access = create_access_token(app=request.app, identity=email, role="APPLICANT")
            refresh = str(uuid.uuid4())
            await RedisConnection.set(
                key=f"{SERVICE_NAME}:user:{email}",
                value={"refresh": refresh},
                expire=SECONDS_FROM_30DAYS
            )
            await RedisConnection.set(
                key=str({"refresh": refresh}),
                value=f"{SERVICE_NAME}:user:{email}",
                expire=SECONDS_FROM_30DAYS
            )
            return json({"access_token": access, "refresh_token": refresh}, status=201)
        elif user_auth.status == 400:
            raise BadRequest
        elif user_auth.status == 403:
            raise Forbidden

    def refresh_token(self, refresh):
        if RedisConnection.get(f"{SERVICE_NAME}:user:{}")
