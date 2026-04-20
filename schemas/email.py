from pydantic import BaseModel, NameEmail
from typing import List

class Email(BaseModel):
    recipients:List[NameEmail]
    subject: str
    body: str
    subtype: str