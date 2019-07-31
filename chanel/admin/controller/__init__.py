from sanic import Blueprint

from chanel.admin.controller.auth import auth_bp

admin_blueprint = Blueprint.group(auth_bp, url_prefix="/api/v1/admin")
