from pydantic import BaseModel, validator, EmailStr
from user_components.user.domain import exceptions


class AddUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_name: str
    password: str
    password_re: str
    phone_number: str
    is_admin: bool = False
    is_customer: bool = False
    is_seller: bool = False

    @validator("password_re")
    def check_password(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("phone_number")
    def check_phone(cls, v):
        if len(v) == 10 and v.isdigit():
            return v
        else:
            raise exceptions.InvalidPhoneNumber


class ActivateUser(BaseModel):
    email: str
    otp: str


class ChangePassword(BaseModel):
    email: str
    password: str
    new_password: str
    new_password_re: str

    @validator("new_password_re")
    def check_password(cls, v, values, **kwargs):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("passwords do not match")
        return v


class ForgetPassword(BaseModel):
    email: str


class ForgetPasswordUpdate(BaseModel):
    email: str
    otp: str
    password_new: str
    password_new_re: str

    @validator("password_new_re")
    def check_password(cls, v, values, **kwargs):
        if "password_new" in values and v != values["password_new"]:
            raise exceptions.PASSWORD_MISMATCHED
        return v


class LoginUser(BaseModel):
    email: str
    password: str


class ResendOtp(BaseModel):
    email: str
