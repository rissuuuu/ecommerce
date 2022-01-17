from sanic import Blueprint
from user_components.user.entrypoints import route_handlers

user = Blueprint("user", url_prefix="api/v1")

user.add_route(route_handlers.UserRoutes.as_view(), "users/<user_id>/")
user.add_route(route_handlers.user_register, "/register_user", methods=["Post"])

user.add_route(route_handlers.user_activate, "/activate_user", methods=["Post"])

user.add_route(route_handlers.user_login, "/login_user", methods=["Post"])

user.add_route(route_handlers.change_password, "/change_password", methods=["Post"])

user.add_route(route_handlers.forgot_password, "/forgot_password", methods=["Post"])

user.add_route(route_handlers.resend_otp, "/resend_otp", methods=["Post"])

user.add_route(
    route_handlers.forget_password_update, "/forgot_password_update", methods=["Post"]
)
