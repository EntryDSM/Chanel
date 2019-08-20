from sanic import Blueprint

from chanel.common.constant import API_VER
from chanel.admin.controller.auth import auth_bp

admin_blueprint = Blueprint.group(auth_bp, url_prefix=f"/api/{API_VER}/admin")
