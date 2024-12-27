import os
import smtplib
from smtplib import SMTP
from email.message import EmailMessage
from server.config.app_configs import app_configs
from jinja2 import Environment, FileSystemLoader, select_autoescape


class Emailer:
    """
    Emailer class to send email
    """
    password: str = app_configs.email_settings.MAIL_PASSWORD
    email: str = app_configs.email_settings.MAIL_USERNAME
    PORT: int = app_configs.email_settings.MAIL_PORT
    SERVER: str = app_configs.email_settings.MAIL_SERVER
    FROM: str = app_configs.email_settings.MAIL_USERNAME

    def __init__(
            self, subject: str,
            to: str,
            template_name: str,
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
        self.server = None
        self.message: EmailMessage = EmailMessage()

    async def enter(self):
        self.server: SMTP = smtplib.SMTP(self.SERVER, self.PORT)
        self.server.starttls()
        self.server.login(self.email, self.password)
        self.message["Subject"] = self.SUBJECT
        self.message["From"] = self.FROM
        self.message["To"] = self.TO
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
