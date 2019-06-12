from sanic import Sanic

from chanel.config import SERVICE_NAME, LOGO
from chanel.config.vault import VaultClient
from chanel.config.listener import initialize


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO
    _app.register_listener(initialize, "before_server_start")

    return _app
