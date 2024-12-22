from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import date
from database import Base

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(100))
    message_id: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(1024))
    message_date: Mapped[date] = mapped_column(Date)
    theme: Mapped[str] = mapped_column(String(100))