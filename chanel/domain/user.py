from chanel.service.user import generate_code
from chanel.repository.connections import RedisConnection


class TempUser:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.code = generate_code()

    def build(self):
        RedisConnection.set(
            key=f"chanel.user.{self.email}",
            value={
                "email": self.email,
                "password": self.password,
                "code": self.code
            }
        )

