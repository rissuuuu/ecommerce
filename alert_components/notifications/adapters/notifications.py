import smtplib
import requests
from entrypoint import settings
from lib.notifications import AbstractNotifications

app_settings = settings.settings_factory()


DEFAULT_EMAIL_HOST = app_settings.email_host
DEFAULT_EMAIL_PORT = app_settings.email_port
DEFAULT_SMS_HOST = app_settings.sms_host
DEBUG = app_settings.debug


class SmsServer:
    def __init__(self, sms_host):
        self.sms_host = sms_host

    async def send_sms(self, to, message):
        if DEBUG is False:
            requests.post(
                self.sms_host,
                data={
                    "token": app_settings.sparrow_sms_token,
                    "from": app_settings.sparrow_sms_from,
                    "to": to,
                    "text": message,
                },
            )
            print("server")
            print(to, message)
            return message
        return message


class SmsNotifications(AbstractNotifications):
    def __init__(self, sms_host=DEFAULT_SMS_HOST):
        self.server = SmsServer(sms_host)

    async def send(self, destination, message):
        sms_message = await self.server.send_sms(to=destination, message=message)
        return sms_message


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host=DEFAULT_EMAIL_HOST, port=DEFAULT_EMAIL_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    async def send(self, destination, message):
        msg = message
        self.server.sendmail(
            from_addr="allocations@example.com",
            to_addrs=[destination],
            msg=msg,
        )
