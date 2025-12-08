import aiosmtplib

from email.message import EmailMessage
from app.config.settings import settings

async def send_verification_email(email: str, verify_url: str, subject: str = "Confirm your account"):

    msg = EmailMessage()
    msg["From"]=f"{settings.MAIL_FROM_NAME}"
    msg["To"]=email
    msg["Subject"]=subject

    text = f"Please confirm your account by visiting: {verify_url}"

    msg.set_content(text)

    await aiosmtplib.send(
        msg,
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
        start_tls=settings.MAIL_STARTTLS
    )
    