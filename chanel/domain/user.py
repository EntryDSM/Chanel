from secrets import token_urlsafe

from chanel.config import SERVICE_NAME
# from chanel.domain import HERMES_ADDRESS
from chanel.repository.connections import RedisConnection


class TempUser:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.code = token_urlsafe(32)

    # def is_conflict_account(self):
    #     url = f"http://{HERMES_ADDRESS}/api/v1/applicant/{self.email}"
    #     response = request(url=url, method="GET").status_code
    #     return False if response == 404 else True

    async def build(self):
        await RedisConnection.set(
            key=f"{SERVICE_NAME}:tempUser:{self.code}",
            value={
                "email": self.email,
                "password": self.password
            }
        )
        await self.send_email()

    async def send_email(self):
        ...
