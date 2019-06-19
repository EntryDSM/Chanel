from sanic import Sanic

from chanel.config import SERVICE_NAME, LOGO
from chanel.config.vault import VaultClient
from chanel.config.listener import initialize
from chanel.controller import signup_bp, user_auth_bp, admin_auth_bp, password_bp


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO
    _app.register_listener(initialize, "before_server_start")

    _app.blueprint(signup_bp)
    _app.blueprint(user_auth_bp)
    _app.blueprint(admin_auth_bp)
    _app.blueprint(password_bp)

    return _app
