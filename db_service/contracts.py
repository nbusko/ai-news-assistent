from pydantic import BaseModel
from datetime import date

class MessageCreate(BaseModel):
    chat_id: str
    message_id: str
    content: str
    message_date: date
    theme: str