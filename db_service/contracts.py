from pydantic import BaseModel
from datetime import date

class MessageCreate(BaseModel):
    chat_id: int
    message_id: int
    content: str
    message_date: date
    theme: str