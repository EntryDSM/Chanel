from sanic import Sanic
from sanic_jwt_extended import JWTManager

from chanel.config import SERVICE_NAME, LOGO
from chanel.config.setting import settings
from chanel.config.vault import VaultClient
from chanel.config.listener import initialize
from chanel.controller import api


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO
    _app.register_listener(initialize, "before_server_start")
    _app.config.JWT_SECRET_KEY = settings.vault_client.get_jwt_secret_key
    JWTManager(_app)

    _app.blueprint(api)

    return _app
