from sanic import Blueprint

from chanel.common.constant import API_VER
from chanel.applicant.controller.auth import auth_bp
from chanel.applicant.controller.signup import signup_bp
from chanel.applicant.controller.password import password_bp

applicant_blueprint = Blueprint.group(
    auth_bp,
    signup_bp,
    password_bp,
    url_prefix=f"/api/{API_VER}/applicant"
)
