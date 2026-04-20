from typing import List

from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import NameEmail

from config.email_config import conf


async def send_email(
    subject: str,
    recipients: List[NameEmail],
    body: str,
    subtype: MessageType | str = MessageType.plain,
):
    if isinstance(subtype, str):
        resolved_subtype = MessageType.plain if subtype == "plain" else MessageType.html
    else:
        resolved_subtype = subtype

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=resolved_subtype,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
