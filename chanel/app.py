import datetime
import os

from entry_logger_sanic import set_logger
from sanic import Blueprint
from sanic import Sanic
from sanic_jwt_extended import JWTManager

from chanel.authentication import user_auth_bp, admin_auth_bp
from chanel.env_variable import SERVICE_NAME
from chanel.password import password_bp
from chanel.setting import LOGO, SETTINGS, initialize
from chanel.signup import signup_bp

LOG_PATH = os.path.dirname(__file__).replace("/chanel", "")


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO
    _app.register_listener(initialize, "before_server_start")
    set_logger(_app, LOG_PATH)

    _app.config["JWT_SECRET_KEY"] = SETTINGS.jwt_secret_key
    _app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
    _app.config["RBAC_ENABLE"] = True
    JWTManager(_app)

    api = Blueprint.group(user_auth_bp, admin_auth_bp, signup_bp, password_bp, url_prefix="/api/v1")
    _app.blueprint(api)

    return _app
