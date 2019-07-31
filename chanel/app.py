import os

from entry_logger_sanic import set_logger
from sanic import Sanic
from sanic_jwt_extended import JWTManager

from chanel.admin.controller import admin_blueprint
from chanel.applicant.controller import applicant_blueprint
from chanel.common.listener import initialize


def create_app():
    _app = Sanic(name="chanel", load_env="CHANEL_")

    log_path = os.path.dirname(__file__).replace("/chanel", "")
    set_logger(_app, log_path)

    _app.register_listener(initialize, "before_server_start")

    _app.blueprint(applicant_blueprint)
    _app.blueprint(admin_blueprint)

    JWTManager(_app)

    return _app
