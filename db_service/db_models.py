from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import date
from database import Base
#Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    message_id: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String(255))
    message_date: Mapped[date] = mapped_column(Date)
    theme: Mapped[str] = mapped_column(String(100))


# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import Text, ForeignKey
# from sqlalchemy.dialects.postgresql import BIGINT

# from database import Base
# # from database import Base


# class IndexMetainfo(Base):
#     __tablename__ = "index_metainfo"

#     index_metainf_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     category: Mapped[str] = mapped_column(Text, nullable=False)
    

# class Texts(Base):
#     __tablename__ = "texts"

#     index_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
#     metainf_id: Mapped[str] = mapped_column(
#         BIGINT, ForeignKey("index_metainfo.index_metainf_id")
#     )

# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import Text, DateTime
# from sqlalchemy.dialects.mysql import BIGINT
# from database import Base

# class Message(Base):
#     __tablename__ = "messages"

#     message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
#     chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
#     message_date: Mapped[DateTime] = mapped_column(nullable=False)
#     message_data: Mapped[str] = mapped_column(Text, nullable=False)
#     message_theme: Mapped[str] = mapped_column(Text, nullable=False)
