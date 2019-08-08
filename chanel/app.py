import os

from entry_logger_sanic import set_logger
from sanic import Sanic
from sanic_jwt_extended import JWTManager

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

    _app.blueprint(applicant_blueprint)
    _app.blueprint(admin_blueprint)

    JWTManager(_app)

    return _app
