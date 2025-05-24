from ..config import app_configs
from ..schemas import ContactUsSchema
from ..utils.email_context import Emailer
from ..events.publisher import publish_contact_us


class ContactUsService:
    @staticmethod
    async def publish(data: ContactUsSchema):
        """
        Publishes the contact us event to the message broker.
        """
        await publish_contact_us(data.model_dump())
        return True

    @staticmethod
    async def contact_us(data: ContactUsSchema):
        await ContactUsService.contact_us_client(data)
        await ContactUsService.contact_us_support(data)
        return

    @staticmethod
    async def contact_us_client(data: ContactUsSchema):
        data = ContactUsSchema.model_validate(data)
        print(data)
        async with Emailer(
            subject=f"Contact Us - {data.subject}",
            template_name="contact_us_template.html",
            to=data.email,
            name=data.name,
            reply_to=app_configs.email_settings.SUPPORT_EMAIL,
            message=data.message
        ) as emailer:
            await emailer.send_message()
        return
    
    @staticmethod
    async def contact_us_support(data: ContactUsSchema):
        data = ContactUsSchema.model_validate(data)
        async with Emailer(
            subject=f"Contact Us - {data.subject}",
            template_name="contact_us_support_template.html",
            to=app_configs.email_settings.SUPPORT_EMAIL,
            name=data.name,
            reply_to=data.email,
            email=data.email,
            message=data.message
        ) as emailer:
            await emailer.send_message()
        return