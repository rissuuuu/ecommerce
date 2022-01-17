
from user_components.user.domain.command import (
    AddUser,
    ActivateUser,
    ChangePassword,
    ForgetPasswordUpdate,
    ForgetPassword,
    LoginUser,
    ResendOtp,
)
from user_components.user.service_layer.handlers import (
    add_user,
    resend_otp,
    activate_user,
    change_password,
    forget_password,
    forget_password_update,
    login_user,
    send_otp_to_user,
)
from user_components.user.domain.events import OTPSent

COMMAND_HANDLERS = {
    AddUser: add_user,
    ActivateUser: activate_user,
    ChangePassword: change_password,
    ForgetPassword: forget_password,
    ForgetPasswordUpdate: forget_password_update,
    LoginUser: login_user,
    ResendOtp: resend_otp,
    }

EVENT_HANDLERS = {
    OTPSent: send_otp_to_user,
}
