import os
import smtplib
from datetime import datetime
from smtplib import SMTP_SSL
from email.message import EmailMessage
from server.config.app_configs import app_configs
from jinja2 import Environment, FileSystemLoader, select_autoescape


class Emailer:
    """
    Emailer class to send email using SSL
    """
    password: str = app_configs.email_settings.MAIL_PASSWORD
    email: str = app_configs.email_settings.MAIL_USERNAME
    PORT: int = app_configs.email_settings.MAIL_PORT  # should be 465 for SSL
    SERVER: str = app_configs.email_settings.MAIL_SERVER
    FROM: str = app_configs.email_settings.MAIL_USERNAME

    def __init__(
        self,
        subject: str,
        to: str,
        template_name: str,
        reply_to: str = None,
        cc: str | list[str] = None,
        **kwargs
    ):
        self.kwargs = kwargs
        self.env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), '../templates')
            ),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.template = self.env.get_template(template_name)
        self.SUBJECT = subject
        self.TO = to
        self.CC = cc
        self.REPLY_TO = reply_to
        self.server = None
        self.message: EmailMessage = EmailMessage()

    async def enter(self):
        self.server: SMTP_SSL = smtplib.SMTP_SSL(self.SERVER, self.PORT)
        self.server.login(self.email, self.password)
        self.message["Subject"] = self.SUBJECT
        self.message["From"] = self.FROM
        self.message["To"] = self.TO

        if self.REPLY_TO:
            self.message["Reply-To"] = self.REPLY_TO

        if self.CC:
            if isinstance(self.CC, list):
                self.message["Cc"] = ", ".join(self.CC)
            else:
                self.message["Cc"] = self.CC

        self.kwargs["current_year"] = datetime.now().year
        self.message.add_alternative(
            self.template.render(**self.kwargs), subtype='html'
        )
        return self

    async def close(self):
        self.message.clear_content()
        self.server.quit()

    async def __aenter__(self):
        await self.enter()
        return self

    async def send_message(self):
        self.server.send_message(self.message)
        await self.close()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.server:
                self.server.quit()
        except smtplib.SMTPServerDisconnected:
            pass
        finally:
            self.message.clear_content()
            self.message.clear()
