import os
import datetime

from sanic import Sanic
from entry_logger_sanic import set_logger
from sanic_jwt_extended import JWTManager

from chanel.common.base_handler import add_error_handlers
from chanel.common.client.vault import settings
from chanel.admin.controller import admin_blueprint
from chanel.applicant.controller import applicant_blueprint
from chanel.common.constant import SERVICE_NAME
from chanel.common.listener import initialize, finalize


def create_app():
    _app = Sanic(name=SERVICE_NAME)

    log_path = os.path.dirname(__file__).replace("/chanel", "")
    set_logger(_app, log_path)

    _app.register_listener(initialize, "before_server_start")
    _app.register_listener(finalize, "after_server_stop")

    add_error_handlers(_app)

    _app.blueprint(applicant_blueprint)
    _app.blueprint(admin_blueprint)

    _app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(int(settings.jwt_access_expire))
    _app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(int(settings.jwt_refresh_expire))
    _app.config['RBAC_ENABLE'] = True

    JWTManager(_app)

    return _app
