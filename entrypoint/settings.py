import os
import typing

from dotenv import find_dotenv, load_dotenv
from pydantic import EmailStr, PostgresDsn

from lib.settings import AbstractSettings

load_dotenv(find_dotenv())
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_HOST = os.environ.get("HOST", "ecom_db")
DB_NAME = os.environ.get("DB_NAME", "app")


class Settings(AbstractSettings):
    pg_dsn: PostgresDsn
    redis_settings: typing.Dict
    components: typing.List[str]
    alembic_config: str
    secret_key: str
    sms_host: str
    sparrow_sms_token: str
    sparrow_sms_from: str
    email_host: str
    email_port: int
    page_size: int
    debug: bool
    SIGN_IN_URL: str
    SIGN_UP_URL: str
    RESEND_URL: str
    POST_FUNDAMENTAL_URL: str
    SEND_OTP: str
    ACTIVATE_USER: str
    mail_user: str
    mail_password: str
    from_email: EmailStr


def settings_factory() -> Settings:
    return Settings(
        pg_dsn=typing.cast(
            PostgresDsn,
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        ),
        redis_settings={"host": "127.0.0.0", "port": "6379"},
        components=[],
        alembic_config="alembic.ini",
        secret_key="2#$%^&SDFGHJKLOIUYTR@#$%^&*987654#$%^&*kJHGF3$%^&*"
        "(kertyujnb345678$%^&*NBVCVBNJHGF$%^&*(JH",
        sms_host="https://api.sparrowsms.com/v2/sms",
        sparrow_sms_token="cH9WDdn9GtgcJXB6cCpF",
        sparrow_sms_from="InfoSMS",
        email_host="smtp.gmail.com",
        email_port=465,
        page_size=5,
        debug=True,
        SIGN_IN_URL="http://127.0.0.1:8000/api/v1/login_user",
        SIGN_UP_URL="http://127.0.0.1:8000/api/v1/register_user/",
        SEND_OTP="http://127.0.0.1:8000/api/v1/resend_otp",
        ACTIVATE_USER="http://127.0.0.1:8000/api/v1/activate_user",
        RESEND_URL="http://127.0.0.1:8000/api/v1/resend_otp",
        POST_FUNDAMENTAL_URL="http://127.0.0.1:8000/api/v1/fundamental_detail/",
        mail_user="19mcmi23@gmail.com",
        mail_password="knlciccalsiqbqyl",
        from_email="19mcmi23@gmail.com",
    )
