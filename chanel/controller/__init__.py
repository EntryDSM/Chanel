from sanic import Blueprint

from chanel.controller.account import SignUp, SignUpVerify
from chanel.controller.authentication import (
    CreateUserToken, RefreshUserToken, DeleteUserToken, CreateAdminToken, RefreshAdminToken, DeleteAdminToken)
from chanel.controller.password import ResetUserPassword

signup_bp = Blueprint("signup", url_prefix="/api/v1/signup")
signup_bp.add_route(SignUp.as_view(), "/")
signup_bp.add_route(SignUpVerify.as_view(), "/verify")

user_auth_bp = Blueprint("user_auth", url_prefix="/api/v1")
user_auth_bp.add_route(CreateUserToken.as_view(), "/login")
user_auth_bp.add_route(RefreshUserToken.as_view(), "/refresh")
user_auth_bp.add_route(DeleteUserToken.as_view(), "/logout")

admin_auth_bp = Blueprint("admin_auth", url_prefix="/api/v1/admin")
admin_auth_bp.add_route(CreateAdminToken.as_view(), "/login")
admin_auth_bp.add_route(RefreshAdminToken.as_view(), "/refresh")
admin_auth_bp.add_route(DeleteAdminToken.as_view(), "/logout")

password_bp = Blueprint("reset_password", url_prefix="/api/v1/password")
password_bp.add_route(ResetUserPassword.as_view(), "/reset")
