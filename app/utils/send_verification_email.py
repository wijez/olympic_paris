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


async def send_password_reset_email(email: str, token: str):
    reset_url = f"http://localhost:8000/reset-password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"""
        Dear User,

        We received a request to reset the password for your account. If you made this request, please click the link below to set a new password:

        Reset your password: {reset_url}

        If you did not request a password reset, please ignore this email.

        Thank you,
        Your Team
        """,
        subtype="plain"
    )

    fm = FastMail(settings.get_email_config())
    await fm.send_message(message)