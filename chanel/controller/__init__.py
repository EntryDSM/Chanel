from sanic import Blueprint

from chanel.controller.account import signup_bp
from chanel.controller.authentication import user_auth_bp, admin_auth_bp
from chanel.controller.password import password_bp

api = Blueprint.group(signup_bp, user_auth_bp, admin_auth_bp, password_bp, url_prefix="/api/v1")
