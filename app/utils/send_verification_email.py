from fastapi_mail import FastMail, MessageSchema

from app.core.email_settings import conf


async def send_verification_email(to_email: str, verify_code: str):
    message = MessageSchema(
        subject="Account Verification",
        recipients=[to_email],
        body=f"Your verification code is: {verify_code}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
