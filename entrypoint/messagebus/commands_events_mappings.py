from user_components.user.domain.command import (
    ActivateUser,
    AddUser,
    ChangePassword,
    ForgetPassword,
    ForgetPasswordUpdate,
    LoginUser,
    ResendOtp,
)
from user_components.user.domain.events import OTPSent
from user_components.user.service_layer.handlers import (
    activate_user,
    add_user,
    change_password,
    forget_password,
    forget_password_update,
    login_user,
    resend_otp,
    send_otp_to_user,
)

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
