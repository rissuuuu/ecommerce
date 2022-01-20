import smtplib

import requests

from entrypoint import settings
from lib.notifications import AbstractNotifications

app_settings = settings.settings_factory()


EMAIL_HOST = app_settings.email_host
EMAIL_PORT = app_settings.email_port
SMS_HOST = app_settings.sms_host
EMAIL_USER = app_settings.mail_user
EMAIL_PASSWORD = app_settings.mail_password
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
    def __init__(self, sms_host=SMS_HOST):
        self.server = SmsServer(sms_host)

    async def send(self, destination, message):
        sms_message = await self.server.send_sms(to=destination, message=message)
        return sms_message


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host=EMAIL_HOST, port=EMAIL_PORT):
        self.server = smtplib.SMTP_SSL(smtp_host, port=port)
        self.server.noop()
        self.server.login(EMAIL_USER,EMAIL_PASSWORD)

    async def send(self, destination, message):
        self.server.sendmail(
            from_addr=EMAIL_USER,
            to_addrs=[destination],
            msg=message,
        )
        self.server.close()
