from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema
from jinja2 import Template
from app.core import settings


async def send_verification_email(to_email: str, verify_code: str):
    try:
        template_path = settings.TEMPLATE_FOLDER / "email.html"
        with open(template_path) as file:
            template = Template(file.read())
        body = template.render(verify_code=verify_code)

        message = MessageSchema(
            subject="Account Verification",
            recipients=[to_email],
            body=body,
            subtype="html"
        )

        fm = FastMail(settings.get_email_config())
        await fm.send_message(message)
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email.")